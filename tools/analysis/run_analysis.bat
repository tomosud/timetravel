@echo off
echo Starting Buy Balance Analysis Visualization...

REM Check if venv_win exists, if not create it
if not exist "..\venv_win" (
    echo Creating virtual environment venv_win...
    cd ..
    python -m venv venv_win
    cd analysis
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call ..\venv_win\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install/update requirements
echo Installing requirements...
pip install -r ..\requirements.txt
if errorlevel 1 (
    echo Failed to install packages.
    pause
    exit /b 1
)

REM Create plots directory
if not exist "plots" (
    echo Creating plots directory...
    mkdir plots
)

REM Run visualization
echo Running buy balance analysis...
python buy_visualizer.py
if errorlevel 1 (
    echo Visualization failed.
    pause
    exit /b 1
)

REM Open plots directory
echo Analysis complete! Opening plots directory...
explorer plots

REM Keep window open
echo.
echo Analysis completed successfully!
echo Check the plots directory for generated visualizations.
pause