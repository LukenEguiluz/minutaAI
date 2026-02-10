@echo off
cd /d "%~dp0"

echo Actualizando cambios...
git pull 2>nul
if %errorlevel% equ 0 (
    echo Cambios actualizados.
) else (
    echo Sin git o ya actualizado. Continuando...
)
echo.

echo Iniciando MinutaAI...
echo.
echo Abre en el navegador: http://localhost:5000
echo Para detener: Ctrl+C
echo.

"venv\Scripts\python.exe" app.py

pause
