#!/usr/bin/env python3
"""
Script de prueba específico para FFmpeg
Verifica que FFmpeg funcione correctamente para MinutaAI
"""

import os
import sys
import subprocess
import tempfile

def test_ffmpeg_installation():
    """Probar instalación de FFmpeg"""
    print("📋 Probando instalación de FFmpeg...")
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg instalado correctamente")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg no encontrado")
    return False

def test_ffprobe():
    """Probar ffprobe"""
    print("\n📋 Probando ffprobe...")
    
    try:
        result = subprocess.run(['ffprobe', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ ffprobe funciona correctamente")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ ffprobe no encontrado")
    return False

def test_audio_generation():
    """Probar generación de audio"""
    print("\n📋 Probando generación de audio...")
    
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            test_file = tmp_file.name
        
        # Generar 3 segundos de audio de prueba
        ffmpeg_cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=3',
            '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
            '-y', test_file
        ]
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True)
        if result.returncode == 0 and os.path.exists(test_file):
            print("✅ Generación de audio exitosa")
            
            # Limpiar archivo temporal
            os.unlink(test_file)
            return True
        else:
            print(f"❌ Error generando audio: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de audio: {e}")
        return False

def test_audio_splitting():
    """Probar división de audio"""
    print("\n📋 Probando división de audio...")
    
    try:
        # Crear archivo de audio de prueba
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            test_file = tmp_file.name
        
        # Generar 10 segundos de audio
        ffmpeg_cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=10',
            '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
            '-y', test_file
        ]
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True)
        if result.returncode != 0:
            print("❌ Error creando archivo de prueba")
            return False
        
        # Obtener duración del archivo
        duration_cmd = [
            'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', test_file
        ]
        
        result = subprocess.run(duration_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Error obteniendo duración")
            os.unlink(test_file)
            return False
        
        duration = float(result.stdout.strip())
        print(f"   Duración del archivo: {duration} segundos")
        
        # Dividir en chunks de 3 segundos
        chunks_created = 0
        for i in range(0, int(duration), 3):
            start_time = i
            end_time = min(i + 3, duration)
            
            chunk_file = f"test_chunk_{chunks_created}.wav"
            
            split_cmd = [
                'ffmpeg', '-i', test_file, '-ss', str(start_time),
                '-t', str(end_time - start_time), '-acodec', 'pcm_s16le',
                '-ar', '16000', '-ac', '1', '-y', chunk_file
            ]
            
            result = subprocess.run(split_cmd, capture_output=True)
            if result.returncode == 0 and os.path.exists(chunk_file):
                chunks_created += 1
                # Limpiar chunk
                os.unlink(chunk_file)
        
        # Limpiar archivo principal
        os.unlink(test_file)
        
        if chunks_created > 0:
            print(f"✅ División de audio exitosa ({chunks_created} chunks creados)")
            return True
        else:
            print("❌ No se pudieron crear chunks")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de división: {e}")
        return False

def test_video_audio_extraction():
    """Probar extracción de audio de video"""
    print("\n📋 Probando extracción de audio de video...")
    
    try:
        # Crear archivo de video de prueba (solo audio)
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as video_file:
            video_path = video_file.name
        
        # Crear archivo de audio de salida
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as audio_file:
            audio_path = audio_file.name
        
        # Generar video de prueba con audio
        video_cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=5',
            '-f', 'lavfi', '-i', 'color=black:size=320x240:duration=5',
            '-c:v', 'libx264', '-c:a', 'aac', '-shortest',
            '-y', video_path
        ]
        
        result = subprocess.run(video_cmd, capture_output=True)
        if result.returncode != 0:
            print("❌ Error creando video de prueba")
            return False
        
        # Extraer audio del video
        extract_cmd = [
            'ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le',
            '-ar', '16000', '-ac', '1', '-y', audio_path
        ]
        
        result = subprocess.run(extract_cmd, capture_output=True)
        if result.returncode == 0 and os.path.exists(audio_path):
            print("✅ Extracción de audio exitosa")
            
            # Limpiar archivos temporales
            os.unlink(video_path)
            os.unlink(audio_path)
            return True
        else:
            print("❌ Error extrayendo audio")
            if os.path.exists(video_path):
                os.unlink(video_path)
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de extracción: {e}")
        return False

def main():
    """Función principal"""
    print("🎬 Pruebas de FFmpeg para MinutaAI")
    print("=" * 40)
    
    tests = [
        ("Instalación de FFmpeg", test_ffmpeg_installation),
        ("ffprobe", test_ffprobe),
        ("Generación de audio", test_audio_generation),
        ("División de audio", test_audio_splitting),
        ("Extracción de audio de video", test_video_audio_extraction),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"❌ Prueba '{test_name}' falló")
    
    print("\n" + "=" * 40)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas de FFmpeg pasaron!")
        print("   FFmpeg está listo para usar con MinutaAI")
    else:
        print("⚠️  Algunas pruebas fallaron")
        print("   Revisa la instalación de FFmpeg")
        print("   Ejecuta: python install_ffmpeg.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)




