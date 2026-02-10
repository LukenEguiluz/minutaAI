import os
import tempfile
import json
import subprocess
import wave
import threading
import math
import numpy as np
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import whisper
from moviepy import VideoFileClip, AudioFileClip
import imageio_ffmpeg
import uuid
from config import get_config

# Obtener configuración
config = get_config()

app = Flask(__name__)
CORS(app)

# Configuración desde archivo config.py
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Crear directorio de uploads si no existe
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

# Estado de trabajos para progreso (job_id -> {status, total_chunks, current_chunk, duration_sec, ...})
jobs = {}
jobs_lock = threading.Lock()


def get_audio_duration_and_chunks(audio_path):
    """Obtener duración en segundos y número de chunks que se crearán. None si error."""
    try:
        with AudioFileClip(audio_path) as clip:
            duration = float(clip.duration)
        if duration <= 0:
            return None
        total_chunks = max(1, math.ceil(duration / config.CHUNK_DURATION))
        return (duration, total_chunks)
    except Exception as e:
        print(f"[MinutaAI] Error obteniendo duración: {e}", flush=True)
        return None

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in config.get_allowed_extensions()

def get_file_type(filename):
    """Determinar si es archivo de audio o video"""
    return config.get_file_type(filename)

def extract_audio_from_video(video_path, output_path):
    """Extraer audio de un archivo de video"""
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(output_path, verbose=False, logger=None)
        video.close()
        return True
    except Exception as e:
        print(f"Error extrayendo audio: {e}")
        return False

def split_audio_into_chunks(audio_path, chunk_duration=None):
    """Dividir audio en chunks usando FFmpeg (el de MoviePy, no depende del PATH)"""
    if chunk_duration is None:
        chunk_duration = config.CHUNK_DURATION

    audio_path = os.path.abspath(audio_path)
    if not os.path.exists(audio_path):
        print(f"Error: archivo de audio no existe: {audio_path}")
        return []

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    try:
        # Obtener duración con MoviePy (no requiere ffprobe en el sistema)
        with AudioFileClip(audio_path) as clip:
            total_duration = float(clip.duration)
        print(f"[MinutaAI] Duración del audio: {total_duration:.1f}s", flush=True)
        if total_duration <= 0:
            print("Error: duración del audio es 0")
            return []

        # Directorio temporal para chunks (ruta absoluta)
        upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
        chunk_dir = os.path.join(upload_dir, "chunks_temp")
        os.makedirs(chunk_dir, exist_ok=True)

        chunks = []
        for i in range(0, int(total_duration) + 1, chunk_duration):
            start_time = i
            end_time = min(i + chunk_duration, total_duration)
            if start_time >= end_time:
                break

            chunk_filename = os.path.join(chunk_dir, f"temp_chunk_{len(chunks)}.wav")
            ffmpeg_cmd = [
                ffmpeg_exe, '-i', audio_path, '-ss', str(start_time),
                '-t', str(end_time - start_time), '-acodec', 'pcm_s16le',
                '-ar', '16000', '-ac', '1', '-y', chunk_filename
            ]
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0 and os.path.exists(chunk_filename):
                chunks.append(chunk_filename)
                if len(chunks) <= 3 or len(chunks) % 5 == 0:
                    print(f"[MinutaAI] Chunk {len(chunks)} creado", flush=True)
            else:
                err = result.stderr or result.stdout or "unknown"
                print(f"Error creando chunk {len(chunks)}: {err[:500]}")
        return chunks
    except Exception as e:
        print(f"Error dividiendo audio: {e}")
        import traceback
        traceback.print_exc()
        return []

def _log_error_to_file(msg, exc=None):
    """Guardar error en archivo para no perderlo si la consola no muestra"""
    try:
        log_path = os.path.join(os.path.dirname(__file__), "minutaai_error.log")
        with open(log_path, "a", encoding="utf-8") as f:
            from datetime import datetime
            f.write(f"\n--- {datetime.now()} ---\n{msg}\n")
            if exc:
                import traceback
                f.write(traceback.format_exc())
    except Exception:
        pass


def _load_wav_as_float32(wav_path):
    """Cargar WAV 16kHz mono a float32. No usa ffmpeg (evita FileNotFoundError en Windows)."""
    try:
        with wave.open(wav_path, "rb") as wav:
            nframes = wav.getnframes()
            if nframes == 0:
                return np.array([], dtype=np.float32)
            buf = wav.readframes(nframes)
            # PCM 16-bit -> float32 en [-1, 1]
            audio = np.frombuffer(buf, dtype=np.int16).astype(np.float32) / 32768.0
            return audio
    except Exception as e:
        print(f"[MinutaAI] Error leyendo WAV {wav_path}: {e}", flush=True)
        return None


def transcribe_chunks(chunks, model, progress_callback=None):
    """Transcribir chunks de audio. progress_callback(current_index_1based, total) opcional."""
    transcriptions = []
    total = len(chunks)
    
    for i, chunk_path in enumerate(chunks):
        chunk_path = os.path.abspath(chunk_path)
        try:
            if not os.path.exists(chunk_path):
                _log(f"Chunk {i} no existe: {chunk_path}")
                transcriptions.append("")
                continue
            size = os.path.getsize(chunk_path)
            if size < 1000:
                _log(f"Chunk {i} muy pequeño ({size} bytes), omitiendo")
                transcriptions.append("")
                try:
                    os.remove(chunk_path)
                except Exception:
                    pass
                continue

            _log(f"Transcribiendo fragmento {i+1}/{len(chunks)}...")
            if progress_callback:
                try:
                    progress_callback(i + 1, total)
                except Exception:
                    pass
            # Cargar WAV con Python (no usa ffmpeg en PATH; los chunks ya son 16kHz mono)
            audio = _load_wav_as_float32(chunk_path)
            if audio is None or audio.size == 0:
                transcriptions.append("")
            else:
                result = model.transcribe(audio, fp16=False)
                transcriptions.append((result.get("text") or "").strip())
            
            try:
                os.remove(chunk_path)
            except Exception:
                pass
            
        except Exception as e:
            import traceback
            err_msg = f"ERROR en chunk {i}: {type(e).__name__}: {e}"
            _log(err_msg)
            _log_error_to_file(err_msg, e)
            traceback.print_exc()
            transcriptions.append(f"[Error en chunk {i}]")
            try:
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)
            except Exception:
                pass
    
    return transcriptions

def _log(msg):
    """Imprimir en consola para que veas el progreso (ventana del .bat)"""
    print(f"[MinutaAI] {msg}", flush=True)

def _run_transcription_job(job_id, file_path, audio_path, file_type, file_extension, unique_id):
    """Ejecutar en segundo plano: dividir, transcribir y actualizar job."""
    with jobs_lock:
        job = jobs.get(job_id)
    if not job:
        return
    try:
        _log("Dividiendo audio en fragmentos...")
        chunks = split_audio_into_chunks(audio_path)
        if not chunks:
            with jobs_lock:
                job["status"] = "error"
                job["error"] = "Error processing audio file"
            return
        with jobs_lock:
            job["total_chunks"] = len(chunks)
            job["step"] = "transcribing"
        _log(f"Fragmentos creados: {len(chunks)}")
        _log("Cargando modelo Whisper (solo la primera vez tarda)...")
        model = whisper.load_model(config.WHISPER_MODEL)
        _log("Modelo cargado. Transcribiendo...")

        def on_chunk_done(current, total):
            with jobs_lock:
                job["current_chunk"] = current
                job["total_chunks"] = total

        transcriptions = transcribe_chunks(chunks, model, progress_callback=on_chunk_done)
        full_transcription = ' '.join(transcriptions)
        txt_filename = f"{unique_id}_transcription.txt"
        txt_path = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(full_transcription)
        if config.CLEANUP_TEMP_FILES and file_type == 'video' and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except Exception:
                pass
        with jobs_lock:
            job["status"] = "done"
            job["transcription"] = full_transcription
            job["txt_file"] = txt_filename
            job["chunks_processed"] = len(chunks)
        _log("Transcripción terminada.")
    except Exception as e:
        import traceback
        _log(f"ERROR: {e}")
        traceback.print_exc()
        with jobs_lock:
            job["status"] = "error"
            job["error"] = str(e)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Subir archivo, calcular chunks y devolver job_id para consultar progreso."""
    try:
        _log("Petición /upload recibida")
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        filename = secure_filename(file.filename)
        _log(f"Archivo: {filename}")
        unique_id = str(uuid.uuid4())
        job_id = str(uuid.uuid4())
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{unique_id}.{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        _log("Guardando archivo en disco...")
        file.save(file_path)
        _log(f"Guardado en: {file_path}")
        
        file_type = get_file_type(filename)
        audio_path = file_path
        if file_type == 'video':
            _log("Es video: extrayendo audio (puede tardar)...")
            audio_path = file_path.replace(file_extension, 'wav')
            if not extract_audio_from_video(file_path, audio_path):
                return jsonify({'error': 'Error extracting audio from video'}), 500
            _log("Audio extraído.")
        
        info = get_audio_duration_and_chunks(audio_path)
        if not info:
            return jsonify({'error': 'No se pudo obtener la duración del audio'}), 500
        duration_sec, total_chunks = info
        _log(f"Duración: {duration_sec:.1f}s → {total_chunks} fragmentos")
        
        with jobs_lock:
            jobs[job_id] = {
                "status": "processing",
                "step": "splitting",
                "total_chunks": total_chunks,
                "current_chunk": 0,
                "duration_sec": round(duration_sec, 1),
                "transcription": None,
                "txt_file": None,
                "error": None,
                "chunks_processed": 0,
            }
        thread = threading.Thread(
            target=_run_transcription_job,
            args=(job_id, file_path, audio_path, file_type, file_extension, unique_id),
            daemon=True,
        )
        thread.start()
        
        return jsonify({
            "job_id": job_id,
            "total_chunks": total_chunks,
            "duration_sec": round(duration_sec, 1),
        })
        
    except Exception as e:
        import traceback
        _log(f"ERROR: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/upload/status/<job_id>')
def upload_status(job_id):
    """Estado del trabajo: total_chunks, current_chunk, status, transcription (si done)."""
    with jobs_lock:
        job = jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    out = {
        "status": job["status"],
        "step": job.get("step", ""),
        "total_chunks": job.get("total_chunks", 0),
        "current_chunk": job.get("current_chunk", 0),
        "duration_sec": job.get("duration_sec", 0),
    }
    if job["status"] == "done":
        out["transcription"] = job.get("transcription", "")
        out["txt_file"] = job.get("txt_file", "")
        out["chunks_processed"] = job.get("chunks_processed", 0)
    if job["status"] == "error":
        out["error"] = job.get("error", "Unknown error")
    return jsonify(out)

@app.route('/download/<filename>')
def download_file(filename):
    """Endpoint para descargar archivos de transcripción"""
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': f'File not found: {str(e)}'}), 404

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Evitar 404 en consola cuando el navegador pide el favicon"""
    return '', 204

@app.route('/health')
def health_check():
    """Endpoint de salud del servidor"""
    return jsonify({'status': 'healthy', 'message': 'Server is running'})

if __name__ == '__main__':
    app.run(
        debug=config.DEBUG, 
        host=config.HOST, 
        port=config.PORT
    ) 