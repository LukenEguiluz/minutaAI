#!/usr/bin/env python3
"""
Script de instalación manual para MinutaAI
Para usar cuando la instalación automática falla
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Imprimir banner de bienvenida"""
    print("🎤" + "="*50)
    print("   MinutaAI - Instalación Manual")
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

def get_pip_path():
    """Obtener ruta de pip"""
    if platform.system().lower() == "windows":
        return os.path.join('venv', 'Scripts', 'pip')
    else:
        return os.path.join('venv', 'bin', 'pip')

def install_basic_dependencies():
    """Instalar dependencias básicas"""
    print("\n📋 Instalando dependencias básicas...")
    
    pip_path = get_pip_path()
    basic_deps = [
        'flask==2.3.3',
        'flask-cors==4.0.0',
        'werkzeug==2.3.7',
        'python-dotenv==1.0.0',
        'requests'
    ]
    
    for dep in basic_deps:
        try:
            print(f"   Instalando {dep}...")
            subprocess.run([pip_path, 'install', dep], check=True)
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error instalando {dep}: {e}")
            return False
    
    print("✅ Dependencias básicas instaladas")
    return True

def install_audio_dependencies():
    """Instalar dependencias de audio"""
    print("\n📋 Instalando dependencias de audio...")
    
    pip_path = get_pip_path()
    audio_deps = [
        'numpy',
        'moviepy==1.0.3'
    ]
    
    for dep in audio_deps:
        try:
            print(f"   Instalando {dep}...")
            subprocess.run([pip_path, 'install', dep], check=True)
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error instalando {dep}: {e}")
            return False
    
    print("✅ Dependencias de audio instaladas")
    return True

def install_whisper():
    """Instalar Whisper"""
    print("\n📋 Instalando Whisper...")
    
    pip_path = get_pip_path()
    
    # Intentar diferentes versiones de Whisper
    whisper_versions = [
        'openai-whisper',
        'openai-whisper==20231117',
        'openai-whisper==20231116',
        'openai-whisper==20231115'
    ]
    
    for version in whisper_versions:
        try:
            print(f"   Intentando instalar {version}...")
            subprocess.run([pip_path, 'install', version], check=True)
            print(f"✅ Whisper instalado: {version}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error con {version}: {e}")
            continue
    
    print("❌ No se pudo instalar Whisper")
    print("\n📋 Soluciones alternativas:")
    print("   1. Instalar manualmente:")
    print("      pip install openai-whisper")
    print("   2. Usar conda:")
    print("      conda install -c conda-forge openai-whisper")
    print("   3. Instalar desde git:")
    print("      pip install git+https://github.com/openai/whisper.git")
    
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
    
    tests = [
        ('flask', 'Flask'),
        ('whisper', 'Whisper'),
        ('moviepy', 'MoviePy')
    ]
    
    all_passed = True
    for module_name, display_name in tests:
        try:
            __import__(module_name)
            print(f"✅ {display_name} - OK")
        except ImportError as e:
            print(f"❌ {display_name} - Error: {e}")
            all_passed = False
    
    return all_passed

def print_instructions():
    """Imprimir instrucciones"""
    print("\n📋 Instrucciones de instalación manual:")
    print("=" * 50)
    
    print("\n1. Activa el entorno virtual:")
    if platform.system().lower() == "windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Instala las dependencias básicas:")
    print("   pip install flask==2.3.3 flask-cors==4.0.0 werkzeug==2.3.7 python-dotenv==1.0.0 requests")
    
    print("\n3. Instala las dependencias de audio:")
    print("   pip install numpy moviepy==1.0.3")
    
    print("\n4. Instala Whisper (prueba una de estas opciones):")
    print("   pip install openai-whisper")
    print("   # o")
    print("   pip install openai-whisper==20231117")
    print("   # o")
    print("   pip install git+https://github.com/openai/whisper.git")
    
    print("\n5. Ejecuta la aplicación:")
    print("   python app.py")
    
    print("\n6. Abre en el navegador:")
    print("   http://localhost:5000")

def main():
    """Función principal"""
    print_banner()
    
    if not check_python_version():
        sys.exit(1)
    
    if not create_virtual_environment():
        print("\n❌ No se pudo crear el entorno virtual")
        sys.exit(1)
    
    print("\n📋 Opciones de instalación:")
    print("   1. Instalación automática (recomendada)")
    print("   2. Instalación manual paso a paso")
    print("   3. Solo mostrar instrucciones")
    
    choice = input("\nSelecciona una opción (1-3): ").strip()
    
    if choice == "1":
        # Instalación automática
        if not install_basic_dependencies():
            print("\n❌ Error en dependencias básicas")
            sys.exit(1)
        
        if not install_audio_dependencies():
            print("\n❌ Error en dependencias de audio")
            sys.exit(1)
        
        if not install_whisper():
            print("\n⚠️  Whisper no se pudo instalar automáticamente")
            print("   Usa las instrucciones manuales a continuación")
        
        if not create_directories():
            sys.exit(1)
        
        if not test_installation():
            print("\n⚠️  Algunas dependencias no están disponibles")
            print("   Revisa los errores anteriores")
        
        print("\n🎉 Instalación completada!")
        print("\n📋 Para ejecutar:")
        print("   1. Activa el entorno virtual")
        print("   2. python app.py")
        print("   3. Abre http://localhost:5000")
        
    elif choice == "2":
        # Instalación manual paso a paso
        print("\n📋 Instalación manual paso a paso:")
        
        print("\nPaso 1: Activa el entorno virtual")
        if platform.system().lower() == "windows":
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        
        input("\nPresiona Enter cuando hayas activado el entorno virtual...")
        
        print("\nPaso 2: Instala dependencias básicas")
        print("   pip install flask==2.3.3 flask-cors==4.0.0 werkzeug==2.3.7 python-dotenv==1.0.0 requests")
        
        input("\nPresiona Enter cuando hayas instalado las dependencias básicas...")
        
        print("\nPaso 3: Instala dependencias de audio")
        print("   pip install numpy moviepy==1.0.3")
        
        input("\nPresiona Enter cuando hayas instalado las dependencias de audio...")
        
        print("\nPaso 4: Instala Whisper")
        print("   pip install openai-whisper")
        
        input("\nPresiona Enter cuando hayas instalado Whisper...")
        
        create_directories()
        
        if test_installation():
            print("\n🎉 ¡Instalación completada!")
        else:
            print("\n⚠️  Algunas dependencias no están disponibles")
            print("   Revisa los errores anteriores")
        
    elif choice == "3":
        # Solo mostrar instrucciones
        print_instructions()
    
    else:
        print("\n❌ Opción no válida")
        sys.exit(1)

if __name__ == "__main__":
    main()
