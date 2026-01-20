@echo off
REM Chess App Launcher for Windows
REM This script activates the virtual environment and runs the chess app

cd /d "%~dp0"

REM Check if .venv exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment and run the app
call .venv\Scripts\activate.bat

REM Run the GUI version
python chessy.py

pause
