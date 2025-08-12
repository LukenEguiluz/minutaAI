# Guía de Contribución

¡Gracias por tu interés en contribuir a MinutaAI! 🎤

## Cómo Contribuir

### 1. Fork del Proyecto

1. Ve a [MinutaAI en GitHub](https://github.com/tu-usuario/MinutaAI)
2. Haz clic en el botón "Fork" en la esquina superior derecha
3. Esto creará una copia del proyecto en tu cuenta de GitHub

### 2. Clona tu Fork

```bash
git clone https://github.com/tu-usuario/MinutaAI.git
cd MinutaAI
```

### 3. Configura el Repositorio Remoto

```bash
git remote add upstream https://github.com/original/MinutaAI.git
```

### 4. Crea una Rama para tu Feature

```bash
git checkout -b feature/nueva-funcionalidad
```

### 5. Instala las Dependencias

```bash
python install.py
```

### 6. Haz tus Cambios

- Escribe código limpio y bien documentado
- Sigue las convenciones de Python (PEP 8)
- Añade comentarios cuando sea necesario
- Actualiza la documentación si es necesario

### 7. Prueba tus Cambios

```bash
# Prueba básica
python test_basic.py

# Prueba de FFmpeg
python test_ffmpeg.py

# Prueba completa
python test_example.py

# Ejecuta la aplicación
python run.py
```

### 8. Commit tus Cambios

```bash
git add .
git commit -m "feat: añadir nueva funcionalidad"
```

### 9. Push a tu Fork

```bash
git push origin feature/nueva-funcionalidad
```

### 10. Crea un Pull Request

1. Ve a tu fork en GitHub
2. Haz clic en "Compare & pull request"
3. Describe tus cambios claramente
4. Envía el PR

## Tipos de Contribuciones

### 🐛 Reportar Bugs

- Usa el template de "Bug report"
- Incluye pasos para reproducir el error
- Añade información del sistema operativo y versión de Python
- Incluye logs de error si es posible

### ✨ Solicitar Features

- Usa el template de "Feature request"
- Describe la funcionalidad que quieres
- Explica por qué sería útil
- Proporciona ejemplos de uso si es posible

### 📝 Mejorar Documentación

- Corrige errores en el README
- Añade ejemplos de uso
- Mejora las instrucciones de instalación
- Traduce documentación a otros idiomas

### 🔧 Mejorar Código

- Optimiza el rendimiento
- Refactoriza código
- Añade tests
- Corrige problemas de seguridad

## Convenciones de Código

### Python

- Sigue PEP 8
- Usa type hints cuando sea posible
- Escribe docstrings para funciones y clases
- Mantén líneas de código bajo 79 caracteres

### Commits

Usa el formato de [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` cambios en documentación
- `style:` cambios de formato
- `refactor:` refactorización de código
- `test:` añadir o corregir tests
- `chore:` cambios en build o herramientas

### Nombres de Ramas

- `feature/nombre-funcionalidad`
- `fix/nombre-bug`
- `docs/nombre-documentacion`
- `refactor/nombre-refactorizacion`

## Estructura del Proyecto

```
MinutaAI/
├── app.py                 # Aplicación principal Flask
├── config.py              # Configuración
├── install.py             # Script de instalación
├── requirements.txt       # Dependencias
├── templates/
│   └── index.html        # Frontend
├── uploads/              # Archivos subidos
├── tests/                # Tests (futuro)
└── docs/                 # Documentación (futuro)
```

## Testing

Antes de enviar un PR, asegúrate de que:

1. Todos los tests pasan
2. La aplicación se ejecuta correctamente
3. No hay errores de linting
4. El código está bien documentado

## Código de Conducta

- Sé respetuoso con otros contribuidores
- Mantén un ambiente inclusivo
- Ayuda a otros cuando puedas
- Reporta comportamiento inapropiado

## Contacto

Si tienes preguntas sobre cómo contribuir:

- Abre un issue en GitHub
- Revisa la documentación existente
- Pregunta en la sección de discusiones

¡Gracias por contribuir a hacer MinutaAI mejor! 🚀
