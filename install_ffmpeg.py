#!/usr/bin/env python3
"""
Script para instalar FFmpeg
Necesario para el procesamiento de audio y video
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Imprimir banner"""
    print("🎬 Instalación de FFmpeg para MinutaAI")
    print("=" * 40)

def check_ffmpeg():
    """Verificar si FFmpeg está instalado"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg ya está instalado")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ FFmpeg no encontrado")
    return False

def install_ffmpeg_windows():
    """Instalar FFmpeg en Windows"""
    print("\n📋 Instalando FFmpeg en Windows...")
    
    # Intentar con chocolatey
    try:
        print("   Intentando con Chocolatey...")
        result = subprocess.run(['choco', 'install', 'ffmpeg', '-y'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg instalado con Chocolatey")
            return True
    except FileNotFoundError:
        print("   Chocolatey no encontrado")
    
    # Intentar con winget
    try:
        print("   Intentando con winget...")
        result = subprocess.run(['winget', 'install', 'FFmpeg'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg instalado con winget")
            return True
    except FileNotFoundError:
        print("   winget no encontrado")
    
    print("\n❌ No se pudo instalar automáticamente")
    print("\n📋 Instalación manual:")
    print("   1. Ve a https://ffmpeg.org/download.html")
    print("   2. Descarga la versión para Windows")
    print("   3. Extrae los archivos")
    print("   4. Añade la carpeta bin al PATH del sistema")
    print("   5. Reinicia la terminal")
    
    return False

def install_ffmpeg_macos():
    """Instalar FFmpeg en macOS"""
    print("\n📋 Instalando FFmpeg en macOS...")
    
    # Intentar con Homebrew
    try:
        print("   Intentando con Homebrew...")
        result = subprocess.run(['brew', 'install', 'ffmpeg'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg instalado con Homebrew")
            return True
    except FileNotFoundError:
        print("   Homebrew no encontrado")
        print("\n📋 Instalar Homebrew primero:")
        print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
    
    return False

def install_ffmpeg_linux():
    """Instalar FFmpeg en Linux"""
    print("\n📋 Instalando FFmpeg en Linux...")
    
    # Detectar distribución
    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read().lower()
            
        if 'ubuntu' in content or 'debian' in content:
            print("   Detectado Ubuntu/Debian")
            result = subprocess.run(['sudo', 'apt', 'update'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                result = subprocess.run(['sudo', 'apt', 'install', '-y', 'ffmpeg'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ FFmpeg instalado con apt")
                    return True
                    
        elif 'fedora' in content or 'rhel' in content or 'centos' in content:
            print("   Detectado Fedora/RHEL/CentOS")
            result = subprocess.run(['sudo', 'dnf', 'install', '-y', 'ffmpeg'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ FFmpeg instalado con dnf")
                return True
                
        elif 'arch' in content:
            print("   Detectado Arch Linux")
            result = subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'ffmpeg'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ FFmpeg instalado con pacman")
                return True
                
    except FileNotFoundError:
        pass
    
    print("\n❌ No se pudo instalar automáticamente")
    print("\n📋 Instalación manual:")
    print("   Ubuntu/Debian: sudo apt install ffmpeg")
    print("   Fedora/RHEL: sudo dnf install ffmpeg")
    print("   Arch Linux: sudo pacman -S ffmpeg")
    
    return False

def main():
    """Función principal"""
    print_banner()
    
    if check_ffmpeg():
        print("\n🎉 FFmpeg está listo para usar!")
        return
    
    system = platform.system().lower()
    
    if system == "windows":
        success = install_ffmpeg_windows()
    elif system == "darwin":  # macOS
        success = install_ffmpeg_macos()
    else:  # Linux
        success = install_ffmpeg_linux()
    
    if success:
        print("\n🎉 ¡FFmpeg instalado exitosamente!")
        print("   Reinicia la terminal y ejecuta: python test_basic.py")
    else:
        print("\n⚠️  Instala FFmpeg manualmente y luego ejecuta:")
        print("   python test_basic.py")

if __name__ == "__main__":
    main()




