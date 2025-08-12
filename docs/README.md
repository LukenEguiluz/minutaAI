# MinutaAI 🎤

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Whisper](https://img.shields.io/badge/Whisper-AI-orange.svg)](https://github.com/openai/whisper)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/tu-usuario/MinutaAI/workflows/CI/badge.svg)](https://github.com/tu-usuario/MinutaAI/actions)

Una aplicación web completa para transcripción automática de archivos de audio y video usando **OpenAI Whisper AI**.

## ✨ Características

- 🎵 **Soporte múltiple de formatos**: Audio (MP3, WAV, M4A, AAC, OGG, FLAC) y Video (MP4, AVI, MOV, MKV, WEBM)
- ⚡ **División automática**: Divide el audio en bloques de 30 segundos para mejor procesamiento
- 🤖 **Transcripción inteligente**: Usa Whisper AI para transcripción precisa
- 🎨 **Interfaz moderna**: Frontend responsive y fácil de usar
- 📥 **Descarga automática**: Genera archivo TXT con la transcripción completa
- ✅ **Validaciones**: Verifica formato y tamaño de archivos
- 🔧 **Instalación automática**: Script que configura todo automáticamente

## 🚀 Instalación Rápida

### Prerrequisitos

- Python 3.8 o superior
- FFmpeg (se instala automáticamente)

### Instalación Automática

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/MinutaAI.git
cd MinutaAI

# Instalación automática
python install.py
```

### Uso

```bash
# Ejecutar la aplicación
python run.py

# Abrir en el navegador
# http://localhost:5000
```

## 📋 Instalación Manual

Si la instalación automática falla, sigue estos pasos:

### 1. Instalar FFmpeg

**Windows:**
```bash
choco install ffmpeg
# o
winget install FFmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update && sudo apt install ffmpeg
```

### 2. Configurar Python

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## 🎯 Uso

1. **Ejecuta la aplicación**:
   ```bash
   python run.py
   ```

2. **Abre tu navegador** en `http://localhost:5000`

3. **Sube un archivo** de audio o video

4. **Espera** a que se complete la transcripción

5. **Descarga** el archivo TXT con la transcripción

## 🛠️ Tecnologías

- **Backend**: Flask 2.3.3
- **IA**: OpenAI Whisper
- **Procesamiento de video**: MoviePy
- **Frontend**: HTML5, CSS3, JavaScript
- **Validación**: Werkzeug

## 📁 Estructura del Proyecto

```
MinutaAI/
├── app.py                 # Aplicación principal Flask
├── config.py              # Configuración
├── install.py             # Script de instalación automática
├── requirements.txt       # Dependencias Python
├── templates/
│   └── index.html        # Interfaz web
├── uploads/              # Archivos subidos (se crea automáticamente)
├── .github/              # GitHub Actions y templates
├── docs/                 # Documentación
└── README.md            # Este archivo
```

## 🔧 Configuración

### Límites de archivo
- **Tamaño máximo**: 500MB
- **Formatos soportados**: Ver lista en la interfaz web

### Modelo Whisper
Cambia el modelo en `app.py` línea 108:
```python
model = whisper.load_model("base")  # Opciones: "tiny", "base", "small", "medium", "large"
```

## 🐛 Solución de Problemas

### Error: "FFmpeg no encontrado"
- Instala FFmpeg siguiendo las instrucciones de arriba
- Asegúrate de que esté en el PATH del sistema

### Error: "Modelo Whisper no encontrado"
- La primera vez descargará automáticamente el modelo
- Asegúrate de tener conexión a internet

### Error: "Error instalando Whisper"
- **Problema**: Whisper puede tener problemas con Python 3.13
- **Solución**: Usa Python 3.11 o 3.12

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee nuestra [Guía de Contribución](CONTRIBUTING.md).

### Cómo contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📊 Rendimiento

- **Tiempo de procesamiento**: Depende del tamaño del archivo y duración
- **Memoria**: El modelo Whisper requiere ~1GB de RAM
- **CPU**: Procesamiento intensivo, recomendado CPU moderna

## 🔒 Seguridad

- Los archivos subidos se almacenan temporalmente
- Se limpian automáticamente después del procesamiento
- No se almacenan transcripciones permanentemente

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- [OpenAI Whisper](https://github.com/openai/whisper) - Modelo de transcripción
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [MoviePy](https://zulko.github.io/moviepy/) - Procesamiento de video

## 📞 Contacto

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/MinutaAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tu-usuario/MinutaAI/discussions)

---

⭐ **Si este proyecto te ayuda, ¡dale una estrella en GitHub!**
