@echo off
setlocal
cd /d "%~dp0"

where pythonw >nul 2>nul
if errorlevel 1 goto :no_pythonw

start "" pythonw "scripts\dashboard_launcher.py"
exit /b 0

:no_pythonw
echo [ERROR] pythonw was not found in PATH.
echo Install Python for Windows and enable "Add Python to PATH", then try again.
pause
exit /b 1
