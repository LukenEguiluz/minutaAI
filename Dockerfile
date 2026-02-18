# MinutaAI - Transcripción de audio/video con Whisper
FROM python:3.11-slim-bookworm

# Instalar FFmpeg (requerido por MoviePy para video)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencias de Python (whisper trae torch, puede tardar en instalar)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Aplicación
COPY app.py config.py ./
COPY templates/ templates/

# Crear directorio de uploads
RUN mkdir -p /app/uploads

# Escuchar en todas las interfaces para acceso desde VPN/externo
ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=5000

EXPOSE 5000

# Persistir uploads con volumen
VOLUME ["/app/uploads"]

CMD ["python", "-u", "app.py"]
