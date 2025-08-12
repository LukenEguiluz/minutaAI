import os
import tempfile
import json
import subprocess
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import whisper
from moviepy.editor import VideoFileClip
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
    """Dividir audio en chunks usando FFmpeg"""
    if chunk_duration is None:
        chunk_duration = config.CHUNK_DURATION
    
    try:
        # Obtener duración del audio usando FFmpeg
        duration_cmd = [
            'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', audio_path
        ]
        result = subprocess.run(duration_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error obteniendo duración: {result.stderr}")
            return []
        
        total_duration = float(result.stdout.strip())
        chunks = []
        
        # Dividir en chunks usando FFmpeg
        for i in range(0, int(total_duration), chunk_duration):
            start_time = i
            end_time = min(i + chunk_duration, total_duration)
            
            # Crear nombre de archivo para el chunk
            chunk_filename = f"temp_chunk_{len(chunks)}.wav"
            
            # Extraer chunk usando FFmpeg
            ffmpeg_cmd = [
                'ffmpeg', '-i', audio_path, '-ss', str(start_time),
                '-t', str(end_time - start_time), '-acodec', 'pcm_s16le',
                '-ar', '16000', '-ac', '1', '-y', chunk_filename
            ]
            
            result = subprocess.run(ffmpeg_cmd, capture_output=True)
            if result.returncode == 0:
                chunks.append(chunk_filename)
            else:
                print(f"Error creando chunk {len(chunks)}: {result.stderr}")
        
        return chunks
    except Exception as e:
        print(f"Error dividiendo audio: {e}")
        return []

def transcribe_chunks(chunks, model):
    """Transcribir chunks de audio"""
    transcriptions = []
    
    for i, chunk_path in enumerate(chunks):
        try:
            # Transcribir directamente el archivo
            result = model.transcribe(chunk_path)
            transcriptions.append(result["text"].strip())
            
            # Limpiar archivo temporal
            if os.path.exists(chunk_path):
                os.remove(chunk_path)
            
        except Exception as e:
            print(f"Error transcribiendo chunk {i}: {e}")
            transcriptions.append(f"[Error en chunk {i}]")
            
            # Limpiar archivo temporal en caso de error
            if os.path.exists(chunk_path):
                os.remove(chunk_path)
    
    return transcriptions

@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint para subir y procesar archivos"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Generar nombre único para el archivo
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{unique_id}.{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Guardar archivo
        file.save(file_path)
        
        # Determinar tipo de archivo
        file_type = get_file_type(filename)
        
        # Si es video, extraer audio
        audio_path = file_path
        if file_type == 'video':
            audio_path = file_path.replace(file_extension, 'wav')
            if not extract_audio_from_video(file_path, audio_path):
                return jsonify({'error': 'Error extracting audio from video'}), 500
        
        # Dividir audio en chunks
        chunks = split_audio_into_chunks(audio_path)
        if not chunks:
            return jsonify({'error': 'Error processing audio file'}), 500
        
        # Cargar modelo Whisper
        model = whisper.load_model(config.WHISPER_MODEL)
        
        # Transcribir chunks
        transcriptions = transcribe_chunks(chunks, model)
        
        # Combinar todas las transcripciones
        full_transcription = ' '.join(transcriptions)
        
        # Guardar transcripción en archivo TXT
        txt_filename = f"{unique_id}_transcription.txt"
        txt_path = os.path.join(app.config['UPLOAD_FOLDER'], txt_filename)
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(full_transcription)
        
        # Limpiar archivos temporales
        if config.CLEANUP_TEMP_FILES:
            if file_type == 'video' and os.path.exists(audio_path):
                os.remove(audio_path)
        
        return jsonify({
            'success': True,
            'message': 'Transcription completed successfully',
            'transcription': full_transcription,
            'txt_file': txt_filename,
            'chunks_processed': len(chunks)
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

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