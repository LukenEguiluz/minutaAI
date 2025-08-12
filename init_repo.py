#!/usr/bin/env python3
"""
Script para inicializar el repositorio Git y prepararlo para GitHub
"""

import os
import subprocess
import sys

def print_banner():
    """Imprimir banner"""
    print("🚀" + "="*60)
    print("   Inicializando Repositorio Git para MinutaAI")
    print("="*60)
    print()

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} completado")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def check_git_installed():
    """Verificar si Git está instalado"""
    print("📋 Verificando Git...")
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        print("✅ Git está instalado")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git no está instalado")
        print("\n📋 Instala Git desde: https://git-scm.com/downloads")
        return False

def initialize_git_repo():
    """Inicializar repositorio Git"""
    if not check_git_installed():
        return False
    
    # Verificar si ya es un repositorio Git
    if os.path.exists('.git'):
        print("✅ Repositorio Git ya existe")
        return True
    
    # Inicializar repositorio
    if not run_command("git init", "Inicializando repositorio Git"):
        return False
    
    return True

def create_gitignore():
    """Verificar que .gitignore existe"""
    if os.path.exists('.gitignore'):
        print("✅ .gitignore ya existe")
        return True
    else:
        print("❌ .gitignore no encontrado")
        return False

def add_files_to_git():
    """Añadir archivos al repositorio"""
    if not run_command("git add .", "Añadiendo archivos al repositorio"):
        return False
    
    # Verificar estado
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("📋 Archivos añadidos:")
        for line in result.stdout.strip().split('\n'):
            if line:
                print(f"   {line}")
    else:
        print("📋 No hay archivos nuevos para añadir")
    
    return True

def make_initial_commit():
    """Hacer commit inicial"""
    return run_command(
        'git commit -m "feat: versión inicial de MinutaAI - Transcripción de Audio/Video con Whisper AI"',
        "Haciendo commit inicial"
    )

def setup_remote_repo():
    """Configurar repositorio remoto"""
    print("\n📋 Configuración del repositorio remoto:")
    print("   1. Ve a https://github.com/new")
    print("   2. Crea un nuevo repositorio llamado 'MinutaAI'")
    print("   3. NO inicialices con README, .gitignore o license (ya los tenemos)")
    print("   4. Copia la URL del repositorio")
    
    repo_url = input("\n📋 Pega la URL del repositorio (ej: https://github.com/tu-usuario/MinutaAI.git): ").strip()
    
    if not repo_url:
        print("❌ URL no proporcionada")
        return False
    
    if not run_command(f'git remote add origin {repo_url}', "Añadiendo repositorio remoto"):
        return False
    
    return True

def push_to_github():
    """Hacer push a GitHub"""
    print("\n📋 Push a GitHub:")
    print("   1. Asegúrate de estar autenticado en GitHub")
    print("   2. Si es la primera vez, configura tu token de acceso personal")
    
    response = input("\n¿Quieres hacer push ahora? (s/N): ").lower()
    if response != 's':
        print("📋 Puedes hacer push manualmente más tarde con:")
        print("   git push -u origin main")
        return True
    
    return run_command("git push -u origin main", "Haciendo push a GitHub")

def print_next_steps():
    """Imprimir próximos pasos"""
    print("\n🎉 ¡Repositorio inicializado!")
    print("\n📋 Próximos pasos:")
    print("   1. Si no hiciste push, ejecuta:")
    print("      git push -u origin main")
    print("\n   2. Configura GitHub Pages (opcional):")
    print("      - Ve a Settings > Pages")
    print("      - Selecciona 'Deploy from a branch'")
    print("      - Selecciona 'main' branch y '/docs' folder")
    print("\n   3. Configura GitHub Actions:")
    print("      - Los workflows ya están configurados")
    print("      - Se ejecutarán automáticamente en cada push")
    print("\n   4. Personaliza el repositorio:")
    print("      - Añade descripción en la página principal")
    print("      - Configura topics: transcription, whisper, audio, video, flask, ai")
    print("      - Añade badges de estado")
    print("\n   5. Invita colaboradores:")
    print("      - Ve a Settings > Collaborators")
    print("      - Añade usuarios que quieras que contribuyan")

def main():
    """Función principal"""
    print_banner()
    
    # Verificaciones y configuración
    if not initialize_git_repo():
        sys.exit(1)
    
    if not create_gitignore():
        print("⚠️  Advertencia: .gitignore no encontrado")
    
    if not add_files_to_git():
        sys.exit(1)
    
    if not make_initial_commit():
        sys.exit(1)
    
    # Configurar remoto
    setup_remote = input("\n¿Quieres configurar el repositorio remoto ahora? (s/N): ").lower()
    if setup_remote == 's':
        if not setup_remote_repo():
            print("❌ Error configurando repositorio remoto")
            print("   Puedes configurarlo manualmente más tarde con:")
            print("   git remote add origin <URL>")
        else:
            push_to_github()
    
    print_next_steps()

if __name__ == "__main__":
    main()
