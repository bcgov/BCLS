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

if "%PY_CMD%"=="" (
  for /d %%D in ("%LocalAppData%\Programs\Python\Python3*") do (
    if exist "%%D\python.exe" set "PY_CMD=%%D\python.exe"
  )
)

if "%PY_CMD%"=="" (
  for /d %%D in ("C:\Program Files\Python3*","C:\Program Files (x86)\Python3*") do (
    if exist "%%D\python.exe" set "PY_CMD=%%D\python.exe"
  )
)

if "%PY_CMD%"=="" goto :no_python
goto :run

:no_python
echo [ERROR] Python was not found.
echo Please install Python 3.11+ from https://www.python.org/downloads/windows/
echo and check "Add Python to PATH" during install.
echo.
echo If Python is already installed, add these folders to User PATH:
echo   1) %%LocalAppData%%\Programs\Python\Python3xx\
echo   2) %%LocalAppData%%\Programs\Python\Python3xx\Scripts\
echo Then open a new terminal and retry.
pause
exit /b 1

:run
echo [INFO] Using Python command: %PY_CMD%
for /f "delims=" %%i in ('%PY_CMD% -c "import sys; print(sys.executable)" 2^>nul') do set "PY_EXE=%%i"
if not "%PY_EXE%"=="" echo [INFO] Python executable: %PY_EXE%
for /f "delims=" %%i in ('%PY_CMD% -V 2^>^&1') do echo [INFO] %%i

call %PY_CMD% -c "import openpyxl" >nul 2>nul
if %errorlevel% neq 0 goto :missing_openpyxl

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

:missing_openpyxl
echo.
echo [ERROR] Python package "openpyxl" is missing.
set /p INSTALL_OXL=Install openpyxl now? (Y/N): 
if /I "%INSTALL_OXL%"=="Y" goto :install_openpyxl
echo Please run this command, then start again:
echo   %PY_CMD% -m pip install --upgrade pip openpyxl
pause
exit /b 1

:install_openpyxl
echo [INFO] Installing openpyxl...
call %PY_CMD% -m pip install --upgrade pip openpyxl
if %errorlevel% neq 0 (
  echo [ERROR] Could not install openpyxl automatically.
  echo Run this manually:
  echo   %PY_CMD% -m pip install --upgrade pip openpyxl
  pause
  exit /b 1
)
echo [OK] openpyxl installed.
goto :run
