@echo off
echo Deteniendo MinutaAI...
echo.

powershell -NoProfile -Command "$p = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; if ($p) { $p | ForEach-Object { Write-Host 'Cerrando PID' $_; Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }; Write-Host ''; Write-Host 'MinutaAI detenido.' } else { Write-Host 'Ningun proceso en puerto 5000.' }"

echo.
pause
