#!/usr/bin/env python3
"""
Script de inicio rápido para MinutaAI
Inicia la aplicación con verificaciones básicas
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Imprimir banner"""
    print("🎤 MinutaAI - Inicio Rápido")
    print("=" * 40)

def check_basic_dependencies():
    """Verificar dependencias básicas"""
    print("📋 Verificando dependencias básicas...")
    
    try:
        import flask
        import moviepy
        print("✅ Dependencias básicas - OK")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        return False

def check_whisper():
    """Verificar Whisper"""
    try:
        import whisper
        print("✅ Whisper - OK")
        return True
    except ImportError:
        print("⚠️  Whisper no está instalado")
        print("   La aplicación funcionará pero sin transcripción")
        return False

def check_ffmpeg():
    """Verificar FFmpeg"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg - OK")
            return True
    except:
        pass
    
    print("⚠️  FFmpeg no encontrado")
    print("   Solo funcionará con archivos de audio")
    return False

def create_directories():
    """Crear directorios necesarios"""
    directories = ['uploads', 'templates']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def start_server():
    """Iniciar servidor"""
    print("\n🚀 Iniciando servidor...")
    print("   URL: http://localhost:5000")
    print("   Presiona Ctrl+C para detener")
    print("-" * 40)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
    except Exception as e:
        print(f"\n❌ Error al iniciar: {e}")
        print("\n📋 Soluciones:")
        print("   1. Verifica que todas las dependencias estén instaladas")
        print("   2. Ejecuta: python install_manual.py")
        print("   3. O instala manualmente:")
        print("      pip install flask flask-cors moviepy numpy")
        print("      pip install openai-whisper")

def main():
    """Función principal"""
    print_banner()
    
    # Verificaciones rápidas
    if not check_basic_dependencies():
        print("\n❌ Dependencias básicas faltantes")
        print("📋 Ejecuta: python install_manual.py")
        sys.exit(1)
    
    check_whisper()
    check_ffmpeg()
    
    create_directories()
    
    # Iniciar servidor
    start_server()

if __name__ == "__main__":
    main()
