@echo off
setlocal

cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python was not found in PATH.
  echo Install Python or add it to PATH, then run this file again.
  pause
  exit /b 1
)

echo [INFO] Starting BC Dashboard Hub server...
start "" "http://localhost:8080/dashboards/bc_dashboard_hub/html/dashboard.html"
python "scripts\serve.py"

endlocal
