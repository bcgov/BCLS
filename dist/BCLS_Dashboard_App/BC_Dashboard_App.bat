@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================
echo   BC Dashboard App
echo ============================================
echo.

if not exist "scripts\serve.py" (
  echo [ERROR] App files are incomplete.
  echo Please unzip the full package again, then retry.
  echo.
  pause
  exit /b 1
)

set "PY_KIND="
set "PY_EXE="

:detect_python
call :auto_detect_python
if defined PY_KIND goto :validate_python

echo [STEP] Python was not found automatically.
echo Please choose:
echo   [1] I know where Python is (enter path)
echo   [2] Show me how to find Python
echo   [3] Exit
set /p "CHOICE=Enter 1, 2, or 3: "
if /I "%CHOICE%"=="1" goto :manual_python
if /I "%CHOICE%"=="2" goto :show_help
if /I "%CHOICE%"=="3" goto :end_fail
echo Invalid choice.
echo.
goto :detect_python

:manual_python
echo.
echo Example path:
echo   C:\Users\YOUR_USER\AppData\Local\Programs\Python\Python312\python.exe
set /p "PY_IN=Paste full python.exe path: "
if "%PY_IN%"=="" (
  echo [WARN] No path entered.
  echo.
  goto :detect_python
)
if not exist "%PY_IN%" (
  echo [ERROR] File not found: %PY_IN%
  echo.
  goto :detect_python
)
set "PY_KIND=exe"
set "PY_EXE=%PY_IN%"
goto :validate_python

:show_help
echo.
echo In Command Prompt, run one of these:
echo   where /r "%%LocalAppData%%\Programs\Python" python.exe
echo   where /r "C:\Program Files" python.exe
echo.
echo If Python is not installed, install it from:
echo   https://www.python.org/downloads/windows/
echo During setup, check: Add Python to PATH
echo.
pause
echo.
goto :detect_python

:validate_python
call :py_exec -V >nul 2>nul
if %errorlevel% neq 0 (
  echo [ERROR] This Python path did not work.
  set "PY_KIND="
  set "PY_EXE="
  echo.
  goto :detect_python
)

echo [OK] Python found.
echo [INFO] Python version:
call :py_exec -V
echo [INFO] Python executable:
call :py_exec -c "import sys; print(sys.executable)"
echo.

call :py_exec -c "import openpyxl" >nul 2>nul
if %errorlevel% neq 0 goto :install_openpyxl
goto :run_server

:install_openpyxl
echo [STEP] One required package is missing: openpyxl
set /p "INS=Install openpyxl now? (Y/N): "
if /I not "%INS%"=="Y" goto :end_fail
echo [INFO] Installing openpyxl...
call :py_exec -m pip install --upgrade pip openpyxl
if %errorlevel% neq 0 (
  echo [ERROR] Automatic install did not work.
  echo Please run this command manually:
  echo   python -m pip install --upgrade pip openpyxl
  echo.
  pause
  exit /b 1
)
echo [OK] openpyxl installed.
echo.
goto :run_server

:run_server
echo [INFO] Checking port 8080...
for /f "tokens=5" %%P in ('netstat -ano ^| findstr /R /C:":8080 .*LISTENING"') do (
  if not "%%P"=="0" (
    echo [INFO] Closing existing process on 8080 (PID %%P)...
    taskkill /PID %%P /F >nul 2>nul
  )
)
echo [INFO] Starting local server...
call :py_exec "scripts\serve.py"
set "EXIT_CODE=%errorlevel%"
echo.
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] Server exited with code %EXIT_CODE%.
  echo Please copy the full error text and share it with support.
)
pause
exit /b %EXIT_CODE%

:auto_detect_python
set "PY_KIND="
set "PY_EXE="
python -V >nul 2>nul
if %errorlevel%==0 (
  set "PY_KIND=python"
  goto :eof
)
py -3 -V >nul 2>nul
if %errorlevel%==0 (
  set "PY_KIND=py"
  goto :eof
)
for /d %%D in ("%LocalAppData%\Programs\Python\Python3*") do (
  if exist "%%D\python.exe" (
    set "PY_KIND=exe"
    set "PY_EXE=%%D\python.exe"
  )
)
if defined PY_KIND goto :eof
for /d %%D in ("C:\Program Files\Python3*" "C:\Program Files (x86)\Python3*") do (
  if exist "%%D\python.exe" (
    set "PY_KIND=exe"
    set "PY_EXE=%%D\python.exe"
  )
)
goto :eof

:py_exec
if "%PY_KIND%"=="python" (
  python %*
  goto :eof
)
if "%PY_KIND%"=="py" (
  py -3 %*
  goto :eof
)
if "%PY_KIND%"=="exe" (
  "%PY_EXE%" %*
  goto :eof
)
exit /b 9009

:end_fail
echo.
echo [INFO] Setup not completed.
echo You can run this file again anytime.
echo.
pause
exit /b 1
