@echo off
REM Time Travel Trading Game - CLI Version Runner
REM Cross-platform Python virtual environment setup and CLI execution

echo Starting Time Travel Trading Game CLI...

REM Check if Windows venv exists, create if not
if not exist "venv_win" (
    echo Creating Windows virtual environment...
    python -m venv venv_win
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv_win\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install requirements if needed
echo Installing/updating requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Run CLI game
echo.
echo Starting CLI version...
python run_cli.py %*

echo.
echo CLI session ended.
pause