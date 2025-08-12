# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD pipeline
- Issue templates para bugs y feature requests
- Pull request template
- Contributing guidelines
- MIT License
- Modern Python packaging configuration

## [1.0.0] - 2024-01-XX

### Added
- Transcripción automática de archivos de audio y video
- Soporte para múltiples formatos de audio (MP3, WAV, M4A, AAC, OGG, FLAC)
- Soporte para múltiples formatos de video (MP4, AVI, MOV, MKV, WEBM)
- Interfaz web moderna y responsive
- División automática de audio en bloques de 30 segundos
- Descarga automática de transcripciones en formato TXT
- Validación de formatos y tamaños de archivo
- Script de instalación automática
- Scripts de prueba para verificar la instalación

### Technical
- Integración con OpenAI Whisper AI
- Backend Flask con CORS habilitado
- Procesamiento de video con MoviePy
- Manejo de archivos con Werkzeug
- Configuración de entorno con python-dotenv
- Límite de tamaño de archivo configurable (500MB por defecto)

### Dependencies
- Flask 2.3.3
- Flask-CORS 4.0.0
- MoviePy 1.0.3
- OpenAI Whisper
- NumPy
- Werkzeug 2.3.7
- python-dotenv 1.0.0
- Requests

## [0.1.0] - 2024-01-XX

### Added
- Versión inicial del proyecto
- Funcionalidad básica de transcripción
- Interfaz web básica
