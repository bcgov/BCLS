@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo   British Columbia Dashboard Suite (Local)
echo ============================================
echo.

where python >nul 2>nul
if %errorlevel%==0 goto :run_python

where py >nul 2>nul
if %errorlevel%==0 goto :run_py_launcher

echo [ERROR] Python was not found.
echo Please install Python 3.11+ and enable "Add Python to PATH".
echo Then run this file again.
pause
exit /b 1

:run_python
python "scripts\serve.py"
goto :eof

:run_py_launcher
py -3 "scripts\serve.py"
goto :eof

