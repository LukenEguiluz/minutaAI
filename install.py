#!/usr/bin/env python3
"""
Script de instalación para MinutaAI
Instala todas las dependencias necesarias
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Imprimir banner de bienvenida"""
    print("🎤" + "="*50)
    print("   MinutaAI - Transcripción de Audio/Video")
    print("="*50)
    print()

def check_python_version():
    """Verificar versión de Python"""
    print("📋 Verificando versión de Python...")
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_ffmpeg():
    """Instalar FFmpeg"""
    print("\n📋 Verificando FFmpeg...")
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg ya está instalado")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg no encontrado")
    system = platform.system().lower()
    
    if system == "windows":
        print("\n📋 Instalación de FFmpeg en Windows:")
        print("   1. Usando Chocolatey (recomendado):")
        print("      choco install ffmpeg")
        print("\n   2. Descarga manual:")
        print("      - Ve a https://ffmpeg.org/download.html")
        print("      - Descarga la versión para Windows")
        print("      - Extrae y añade al PATH")
        
    elif system == "darwin":  # macOS
        print("\n📋 Instalación de FFmpeg en macOS:")
        print("   brew install ffmpeg")
        
    else:  # Linux
        print("\n📋 Instalación de FFmpeg en Linux:")
        print("   sudo apt update && sudo apt install ffmpeg")
    
    response = input("\n¿Quieres continuar sin FFmpeg? (s/N): ").lower()
    return response == 's'

def create_virtual_environment():
    """Crear entorno virtual"""
    print("\n📋 Creando entorno virtual...")
    
    if os.path.exists('venv'):
        print("✅ Entorno virtual ya existe")
        return True
    
    try:
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        print("✅ Entorno virtual creado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando entorno virtual: {e}")
        return False

def activate_virtual_environment():
    """Activar entorno virtual"""
    print("\n📋 Activando entorno virtual...")
    
    if platform.system().lower() == "windows":
        activate_script = os.path.join('venv', 'Scripts', 'activate')
    else:
        activate_script = os.path.join('venv', 'bin', 'activate')
    
    if not os.path.exists(activate_script):
        print("❌ Script de activación no encontrado")
        return False
    
    print("✅ Entorno virtual activado")
    print("\n📋 Para activar manualmente:")
    if platform.system().lower() == "windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    return True

def install_dependencies():
    """Instalar dependencias de Python"""
    print("\n📋 Instalando dependencias...")
    
    try:
        # Usar pip del entorno virtual
        if platform.system().lower() == "windows":
            pip_path = os.path.join('venv', 'Scripts', 'pip')
        else:
            pip_path = os.path.join('venv', 'bin', 'pip')
        
        # Actualizar pip primero
        subprocess.run([pip_path, 'install', '--upgrade', 'pip'], check=True)
        print("✅ Pip actualizado")
        
        # Instalar dependencias una por una para mejor control de errores
        dependencies = [
            'flask==2.3.3',
            'flask-cors==4.0.0',
            'moviepy==1.0.3',
            'numpy',
            'werkzeug==2.3.7',
            'python-dotenv==1.0.0',
            'requests'
        ]
        
        for dep in dependencies:
            print(f"   Instalando {dep}...")
            subprocess.run([pip_path, 'install', dep], check=True)
        
        # Instalar Whisper por separado (puede ser problemático)
        print("   Instalando openai-whisper...")
        try:
            subprocess.run([pip_path, 'install', 'openai-whisper'], check=True)
        except subprocess.CalledProcessError:
            print("   ⚠️  Error con Whisper, intentando con versión específica...")
            subprocess.run([pip_path, 'install', 'openai-whisper==20231117'], check=True)
        
        print("✅ Dependencias instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        print("\n📋 Solución alternativa:")
        print("   1. Activa el entorno virtual:")
        if platform.system().lower() == "windows":
            print("      venv\\Scripts\\activate")
        else:
            print("      source venv/bin/activate")
        print("   2. Instala manualmente:")
        print("      pip install flask flask-cors moviepy numpy werkzeug python-dotenv requests")
        print("      pip install openai-whisper")
        return False

def create_directories():
    """Crear directorios necesarios"""
    print("\n📋 Creando directorios...")
    
    directories = ['uploads', 'templates']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directorio '{directory}' creado")
    
    return True

def test_installation():
    """Probar la instalación"""
    print("\n📋 Probando instalación...")
    
    try:
        # Importar módulos principales
        import flask
        import whisper
        import moviepy
        
        print("✅ Todas las dependencias están disponibles")
        return True
    except ImportError as e:
        print(f"❌ Error importando dependencias: {e}")
        return False

def print_next_steps():
    """Imprimir próximos pasos"""
    print("\n🎉 ¡Instalación completada!")
    print("\n📋 Próximos pasos:")
    print("   1. Activa el entorno virtual:")
    if platform.system().lower() == "windows":
        print("      venv\\Scripts\\activate")
    else:
        print("      source venv/bin/activate")
    
    print("\n   2. Ejecuta la aplicación:")
    print("      python run.py")
    print("      # o")
    print("      python app.py")
    
    print("\n   3. Abre tu navegador en:")
    print("      http://localhost:5000")
    
    print("\n📚 Para más información, consulta README.md")

def main():
    """Función principal"""
    print_banner()
    
    # Verificaciones
    if not check_python_version():
        sys.exit(1)
    
    if not install_ffmpeg():
        print("\n⚠️  Advertencia: FFmpeg es necesario para procesar videos")
        print("   La aplicación funcionará solo con archivos de audio")
    
    # Instalación
    if not create_virtual_environment():
        sys.exit(1)
    
    if not activate_virtual_environment():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not create_directories():
        sys.exit(1)
    
    if not test_installation():
        print("\n❌ Error en la instalación. Revisa los errores anteriores.")
        sys.exit(1)
    
    print_next_steps()

if __name__ == "__main__":
    main() 