#!/usr/bin/env python3
"""
Script de inicio para MinutaAI
Ejecuta la aplicación con configuraciones optimizadas
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} - OK")

def check_ffmpeg():
    """Verificar si FFmpeg está instalado"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg encontrado - OK")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg no encontrado")
    print("\n📋 Instalación de FFmpeg:")
    
    system = platform.system().lower()
    if system == "windows":
        print("   Opción 1: choco install ffmpeg")
        print("   Opción 2: Descargar desde https://ffmpeg.org/download.html")
    elif system == "darwin":  # macOS
        print("   brew install ffmpeg")
    else:  # Linux
        print("   sudo apt update && sudo apt install ffmpeg")
    
    return False

def check_dependencies():
    """Verificar dependencias de Python"""
    try:
        import flask
        import whisper
        import pydub
        import moviepy
        print("✅ Dependencias Python - OK")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("\n📋 Instalar dependencias:")
        print("   pip install -r requirements.txt")
        return False

def create_directories():
    """Crear directorios necesarios"""
    directories = ['uploads', 'templates']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directorios creados - OK")

def main():
    """Función principal"""
    print("🎤 MinutaAI - Transcripción de Audio/Video")
    print("=" * 50)
    
    # Verificaciones
    check_python_version()
    
    if not check_ffmpeg():
        print("\n⚠️  Advertencia: FFmpeg es necesario para procesar videos")
        print("   Puedes continuar, pero solo funcionará con archivos de audio")
        response = input("   ¿Continuar sin FFmpeg? (s/N): ").lower()
        if response != 's':
            sys.exit(1)
    
    if not check_dependencies():
        print("\n❌ Instala las dependencias antes de continuar")
        sys.exit(1)
    
    create_directories()
    
    print("\n🚀 Iniciando servidor...")
    print("   URL: http://localhost:5000")
    print("   Presiona Ctrl+C para detener")
    print("-" * 50)
    
    # Ejecutar aplicación
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
    except Exception as e:
        print(f"\n❌ Error al iniciar: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 