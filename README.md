# MinutaAI - Transcripción de Audio/Video

Una aplicación web completa para transcripción automática de archivos de audio y video usando Whisper AI.

## 🚀 Características

- **Soporte múltiple de formatos**: Audio (MP3, WAV, M4A, AAC, OGG, FLAC) y Video (MP4, AVI, MOV, MKV, WEBM)
- **División automática**: Divide el audio en bloques de 30 segundos para mejor procesamiento
- **Transcripción inteligente**: Usa Whisper AI para transcripción precisa
- **Interfaz moderna**: Frontend responsive y fácil de usar
- **Descarga automática**: Genera archivo TXT con la transcripción completa
- **Validaciones**: Verifica formato y tamaño de archivos

## 📋 Requisitos

- Python 3.8 o superior
- FFmpeg (para procesamiento de video)

### Instalación de FFmpeg

**Opción 1: Instalación automática**
```bash
python install_ffmpeg.py
```

**Opción 2: Instalación manual**

**Windows:**
```bash
# Usando chocolatey
choco install ffmpeg

# O usando winget
winget install FFmpeg

# O descargar desde https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

## 🛠️ Instalación

### Opción 1: Instalación Automática (Recomendada)

1. **Clonar o descargar el proyecto**
```bash
git clone <repository-url>
cd MinutaAI
```

2. **Ejecutar script de instalación**
```bash
python install.py
```

### Opción 2: Instalación Manual

Si la instalación automática falla, usa el script manual:

```bash
python install_manual.py
```

### Opción 3: Instalación Manual Paso a Paso

1. **Crear entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

2. **Instalar dependencias básicas**
```bash
pip install flask==2.3.3 flask-cors==4.0.0 werkzeug==2.3.7 python-dotenv==1.0.0 requests
```

3. **Instalar dependencias de audio**
```bash
pip install numpy moviepy==1.0.3
```

4. **Instalar Whisper (prueba una de estas opciones)**
```bash
pip install openai-whisper
# o
pip install openai-whisper==20231117
# o
pip install git+https://github.com/openai/whisper.git
```

## 🐳 Docker (hostear en PC / VPN / dominio)

Para ejecutar MinutaAI en un contenedor Docker y exponerlo en tu red o VPN:

```bash
# Construir y ejecutar
docker compose up -d

# Ver logs
docker compose logs -f minutaai
```

La app estará disponible en `http://localhost:5000` y escucha en todas las interfaces (`0.0.0.0`), por lo que es accesible desde otros dispositivos en tu red local y desde tu VPN.

**Puentear a un dominio**: Usa un túnel (Cloudflare Tunnel, ngrok, Tailscale) o un reverse proxy (nginx, Caddy) en tu PC para apuntar tu dominio al puerto 5000. Ver [DOCKER.md](DOCKER.md) para más detalles.

## 🚀 Uso

### Verificar Instalación

Antes de usar la aplicación, verifica que todo esté funcionando:

```bash
# Prueba básica (sin Whisper)
python test_basic.py

# Prueba de FFmpeg
python test_ffmpeg.py

# Prueba completa (con Whisper)
python test_example.py
```

### Ejecutar la Aplicación

**Opción 1: Inicio rápido (recomendado)**
```bash
python quick_start.py
```

**Opción 2: Inicio estándar**
```bash
python app.py
# o
python run.py
```

2. **Abrir en el navegador**
```
http://localhost:5000
```

3. **Usar la aplicación**
   - Arrastra un archivo de audio o video al área de subida
   - O haz clic para seleccionar un archivo
   - Haz clic en "Transcribir"
   - Espera a que se complete el procesamiento
   - Descarga el archivo TXT con la transcripción

## 📁 Estructura del Proyecto

```
MinutaAI/
├── app.py                 # Backend Flask
├── requirements.txt       # Dependencias Python
├── templates/
│   └── index.html        # Frontend
├── uploads/              # Archivos subidos (se crea automáticamente)
└── README.md            # Este archivo
```

## 🔧 Configuración

### Límites de archivo
- Tamaño máximo: 500MB
- Formatos soportados: Ver lista en la interfaz web

### Modelo Whisper
- Por defecto usa el modelo "base" de Whisper
- Puedes cambiar el modelo en `app.py` línea 108:
```python
model = whisper.load_model("base")  # Opciones: "tiny", "base", "small", "medium", "large"
```

## 🐛 Solución de Problemas

### Error: "No se puede conectar con el servidor"
- Verifica que el servidor esté ejecutándose en `http://localhost:5000`
- Revisa que no haya otro proceso usando el puerto 5000

### Error: "FFmpeg no encontrado"
- Instala FFmpeg siguiendo las instrucciones de arriba
- Asegúrate de que FFmpeg esté en el PATH del sistema

### Error: "Modelo Whisper no encontrado"
- La primera vez que ejecutes la aplicación, descargará automáticamente el modelo
- Asegúrate de tener conexión a internet

### Error: "Error instalando Whisper"
- **Problema**: Whisper puede tener problemas de compatibilidad con Python 3.13
- **Solución 1**: Usar Python 3.11 o 3.12
- **Solución 2**: Instalar Whisper manualmente:
  ```bash
  pip install openai-whisper
  ```
- **Solución 3**: Usar conda:
  ```bash
  conda install -c conda-forge openai-whisper
  ```
- **Solución 4**: Instalar desde git:
  ```bash
  pip install git+https://github.com/openai/whisper.git
  ```

### Error: "Archivo demasiado grande"
- El límite es 500MB por archivo
- Considera dividir archivos muy grandes

## 📊 Rendimiento

- **Tiempo de procesamiento**: Depende del tamaño del archivo y la duración
- **Memoria**: El modelo Whisper requiere aproximadamente 1GB de RAM
- **CPU**: Procesamiento intensivo, recomendado usar CPU moderna

## 🔒 Seguridad

- Los archivos subidos se almacenan temporalmente
- Se limpian automáticamente después del procesamiento
- No se almacenan transcripciones permanentemente

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- [OpenAI Whisper](https://github.com/openai/whisper) - Modelo de transcripción
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [MoviePy](https://zulko.github.io/moviepy/) - Procesamiento de video
- [Pydub](https://github.com/jiaaro/pydub) - Procesamiento de audio 