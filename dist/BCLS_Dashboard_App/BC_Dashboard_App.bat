@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo   British Columbia Dashboard Suite (Local)
echo ============================================
echo.

if not exist "scripts\serve.py" (
  echo [ERROR] Could not find scripts\serve.py
  echo Make sure the zip was fully extracted and folder structure is intact.
  pause
  exit /b 1
)

set "PY_CMD="
python -V >nul 2>nul
if %errorlevel%==0 set "PY_CMD=python"

if "%PY_CMD%"=="" (
  py -3 -V >nul 2>nul
  if %errorlevel%==0 set "PY_CMD=py -3"
)

if "%PY_CMD%"=="" goto :no_python
goto :run

:no_python
echo [ERROR] Python was not found.
echo Please install Python 3.11+ from https://www.python.org/downloads/windows/
echo and check "Add Python to PATH" during install.
echo.
echo If Python is already installed, disable Windows "App execution aliases"
echo for python.exe / python3.exe, then run this file again.
pause
exit /b 1

:run
echo [INFO] Starting local server...
call %PY_CMD% "scripts\serve.py"
set "EXIT_CODE=%errorlevel%"
if not "%EXIT_CODE%"=="0" (
  echo.
  echo [ERROR] Server exited with code %EXIT_CODE%.
  echo If this keeps happening, run this command manually and send the full error:
  echo   python scripts\serve.py
)
echo.
pause
exit /b %EXIT_CODE%
