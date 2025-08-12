#!/usr/bin/env python3
"""
Script de prueba básica para MinutaAI
Verifica que los componentes principales funcionen sin Whisper
"""

import os
import sys
import subprocess
import platform

def test_python_version():
    """Probar versión de Python"""
    print("📋 Probando versión de Python...")
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def test_basic_dependencies():
    """Probar dependencias básicas"""
    print("\n📋 Probando dependencias básicas...")
    
    basic_deps = [
        ('flask', 'Flask'),
        ('werkzeug', 'Werkzeug'),
        ('requests', 'Requests')
    ]
    
    all_passed = True
    for module_name, display_name in basic_deps:
        try:
            __import__(module_name)
            print(f"✅ {display_name} - OK")
        except ImportError as e:
            print(f"❌ {display_name} - Error: {e}")
            all_passed = False
    
    return all_passed

def test_audio_dependencies():
    """Probar dependencias de audio"""
    print("\n📋 Probando dependencias de audio...")
    
    audio_deps = [
        ('moviepy', 'MoviePy'),
        ('numpy', 'NumPy')
    ]
    
    all_passed = True
    for module_name, display_name in audio_deps:
        try:
            __import__(module_name)
            print(f"✅ {display_name} - OK")
        except ImportError as e:
            print(f"❌ {display_name} - Error: {e}")
            all_passed = False
    
    return all_passed

def test_whisper():
    """Probar Whisper"""
    print("\n📋 Probando Whisper...")
    
    try:
        import whisper
        print("✅ Whisper - OK")
        return True
    except ImportError as e:
        print(f"❌ Whisper - Error: {e}")
        print("   ⚠️  Whisper no está instalado, pero puedes continuar")
        print("   📋 Para instalar Whisper:")
        print("      pip install openai-whisper")
        return False

def test_ffmpeg():
    """Probar FFmpeg"""
    print("\n📋 Probando FFmpeg...")
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg - OK")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg no encontrado")
    print("   ⚠️  FFmpeg es necesario para procesar videos")
    print("   📋 Para instalar FFmpeg:")
    system = platform.system().lower()
    if system == "windows":
        print("      choco install ffmpeg")
    elif system == "darwin":
        print("      brew install ffmpeg")
    else:
        print("      sudo apt install ffmpeg")
    return False

def test_file_processing():
    """Probar procesamiento de archivos"""
    print("\n📋 Probando procesamiento de archivos...")
    
    try:
        # Crear archivo de audio de prueba usando FFmpeg
        test_file = "test_audio.wav"
        
        # Generar 5 segundos de audio de prueba usando FFmpeg
        ffmpeg_cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=5',
            '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
            '-y', test_file
        ]
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True)
        if result.returncode != 0:
            print(f"❌ Error generando audio de prueba: {result.stderr}")
            return False
        
        # Verificar que el archivo se creó
        if not os.path.exists(test_file):
            print("❌ Archivo de prueba no se creó")
            return False
        
        print(f"✅ Procesamiento de archivos - OK")
        
        # Limpiar archivo de prueba
        os.remove(test_file)
        return True
        
    except Exception as e:
        print(f"❌ Error en procesamiento de archivos: {e}")
        if os.path.exists("test_audio.wav"):
            os.remove("test_audio.wav")
        return False

def test_flask_app():
    """Probar aplicación Flask"""
    print("\n📋 Probando aplicación Flask...")
    
    try:
        from app import app
        print("✅ Aplicación Flask - OK")
        return True
    except Exception as e:
        print(f"❌ Error en aplicación Flask: {e}")
        return False

def run_basic_tests():
    """Ejecutar pruebas básicas"""
    print("🧪 Ejecutando pruebas básicas de MinutaAI")
    print("=" * 50)
    
    tests = [
        ("Python", test_python_version),
        ("Dependencias básicas", test_basic_dependencies),
        ("Dependencias de audio", test_audio_dependencies),
        ("FFmpeg", test_ffmpeg),
        ("Procesamiento de archivos", test_file_processing),
        ("Aplicación Flask", test_flask_app),
        ("Whisper", test_whisper),
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
    
    if passed >= total - 1:  # Permitir que Whisper falle
        print("🎉 ¡Pruebas básicas pasaron! La aplicación está lista para usar.")
        print("\n📋 Para ejecutar la aplicación:")
        print("   python app.py")
        print("   # o")
        print("   python run.py")
        
        if passed < total:
            print("\n⚠️  Nota: Whisper no está instalado")
            print("   Para transcripción, instala Whisper:")
            print("   pip install openai-whisper")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores anteriores.")
        print("\n📋 Para obtener ayuda:")
        print("   python install_manual.py")
    
    return passed >= total - 1

if __name__ == "__main__":
    success = run_basic_tests()
    sys.exit(0 if success else 1)
