#!/usr/bin/env python3
"""
Script de prueba para MinutaAI
Verifica que todos los componentes funcionen correctamente
"""

import os
import sys
import subprocess
import requests
import time

def test_dependencies():
    """Probar dependencias"""
    print("📋 Probando dependencias...")
    
    try:
        import flask
        import whisper
        import pydub
        import moviepy
        print("✅ Todas las dependencias están disponibles")
        return True
    except ImportError as e:
        print(f"❌ Error: {e}")
        return False

def test_ffmpeg():
    """Probar FFmpeg"""
    print("\n📋 Probando FFmpeg...")
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg funciona correctamente")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg no está disponible")
    return False

def test_server():
    """Probar servidor"""
    print("\n📋 Probando servidor...")
    
    try:
        # Intentar conectar al servidor
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Servidor responde correctamente")
            return True
    except requests.exceptions.RequestException:
        pass
    
    print("❌ Servidor no responde")
    print("   Asegúrate de que el servidor esté ejecutándose:")
    print("   python app.py")
    return False

def test_whisper_model():
    """Probar modelo Whisper"""
    print("\n📋 Probando modelo Whisper...")
    
    try:
        import whisper
        model = whisper.load_model("base")
        print("✅ Modelo Whisper cargado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error cargando modelo Whisper: {e}")
        return False

def test_file_processing():
    """Probar procesamiento de archivos"""
    print("\n📋 Probando procesamiento de archivos...")
    
    # Crear archivo de prueba
    test_file = "test_audio.wav"
    
    try:
        from pydub import AudioSegment
        from pydub.generators import Sine
        
        # Generar 5 segundos de audio de prueba
        audio = Sine(440).to_audio_segment(duration=5000)
        audio.export(test_file, format="wav")
        
        # Probar división en chunks
        audio_segment = AudioSegment.from_file(test_file)
        chunks = []
        chunk_length_ms = 30000  # 30 segundos
        
        for i in range(0, len(audio_segment), chunk_length_ms):
            chunk = audio_segment[i:i + chunk_length_ms]
            chunks.append(chunk)
        
        print(f"✅ Procesamiento de archivos funciona ({len(chunks)} chunks creados)")
        
        # Limpiar archivo de prueba
        os.remove(test_file)
        return True
        
    except Exception as e:
        print(f"❌ Error en procesamiento de archivos: {e}")
        if os.path.exists(test_file):
            os.remove(test_file)
        return False

def run_full_test():
    """Ejecutar todas las pruebas"""
    print("🧪 Ejecutando pruebas completas de MinutaAI")
    print("=" * 50)
    
    tests = [
        ("Dependencias", test_dependencies),
        ("FFmpeg", test_ffmpeg),
        ("Modelo Whisper", test_whisper_model),
        ("Procesamiento de archivos", test_file_processing),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"❌ Prueba '{test_name}' falló")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La aplicación está lista para usar.")
        print("\n📋 Para ejecutar la aplicación:")
        print("   python app.py")
        print("   # o")
        print("   python run.py")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores anteriores.")
        print("\n📋 Para obtener ayuda:")
        print("   python install.py")
    
    return passed == total

if __name__ == "__main__":
    success = run_full_test()
    sys.exit(0 if success else 1) 