@echo off
echo Setting up Windows Python environment...

REM Check if venv_win exists, if not create it
if not exist "venv_win" (
    echo Creating virtual environment venv_win...
    python -m venv venv_win
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv_win\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install/update requirements
echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install packages.
    pause
    exit /b 1
)

REM Launch browser (background)
echo Starting browser...
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:5000"

REM Start game server
echo Starting game server...
echo ============================================
echo   Game URL: http://127.0.0.1:5000
echo   To quit: Press Ctrl+C
echo ============================================
python entry.py

REM Post-server shutdown processing
echo.
echo Game server has been terminated.
pause