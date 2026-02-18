"""
Configuración de MinutaAI
"""

import os

class Config:
    """Configuración base"""
    
    # Configuración del servidor
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    
    # Configuración de archivos
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
    
    # Formatos permitidos
    ALLOWED_AUDIO_EXTENSIONS = {
        'mp3', 'wav', 'm4a', 'aac', 'ogg', 'flac', 'wma'
    }
    
    ALLOWED_VIDEO_EXTENSIONS = {
        'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'm4v'
    }
    
    # Configuración de Whisper (puede sobrescribirse con env WHISPER_MODEL)
    WHISPER_MODEL = os.environ.get('WHISPER_MODEL', 'base')  # tiny, base, small, medium, large
    
    # Configuración de chunks (audios largos: se dividen en bloques, se transcriben y se unen al final)
    CHUNK_DURATION = 30  # segundos por bloque (15–30 recomendado; menor = más preciso, más lento)
    
    # Configuración de limpieza
    CLEANUP_TEMP_FILES = True
    
    @classmethod
    def get_allowed_extensions(cls):
        """Obtener todas las extensiones permitidas"""
        return cls.ALLOWED_AUDIO_EXTENSIONS.union(cls.ALLOWED_VIDEO_EXTENSIONS)
    
    @classmethod
    def get_file_type(cls, filename):
        """Determinar tipo de archivo basado en extensión"""
        if '.' not in filename:
            return None
        
        ext = filename.rsplit('.', 1)[1].lower()
        
        if ext in cls.ALLOWED_AUDIO_EXTENSIONS:
            return 'audio'
        elif ext in cls.ALLOWED_VIDEO_EXTENSIONS:
            return 'video'
        
        return None

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtener configuración basada en variable de entorno"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default']) 