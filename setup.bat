@echo off
setlocal
cd /d "%~dp0"

REM Optional: pass a version like "0.28.3" as the first arg. Blank means latest.
set "FLET_VERSION=%~1"
if "%FLET_VERSION%"=="" (
    set "FLET_PKG=flet flet-desktop"
    set "FLET_LABEL=latest"
    ) else (
    set "FLET_PKG=flet==%FLET_VERSION% flet-desktop==%FLET_VERSION%"
    set "FLET_LABEL=%FLET_VERSION%"
)

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found.
    pause
    exit /b
)

REM Create venv
if not exist "venv" (
    python -m venv venv
)

REM Activate venv & install/upgrade flet
call venv\Scripts\activate
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [ERROR] pip upgrade failed.
    pause
    exit /b
)

echo Installing Flet (%FLET_LABEL%)...
pip install --upgrade %FLET_PKG%
if %errorlevel% neq 0 (
    echo [ERROR] Flet install failed.
    pause
    exit /b
)

REM Create launcher if not exists
if not exist "run_app.bat" (
    echo @echo off > run_app.bat
    echo cd /d "%%~dp0" >> run_app.bat
    echo call venv\Scripts\activate >> run_app.bat
    echo start /b pythonw app.py >> run_app.bat
)

echo Setup complete. Use run_app.bat to start app.
pause
endlocal
