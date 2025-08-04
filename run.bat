@echo off
title AI Energy Optimizer - Starting...
color 0A

echo.
echo ========================================
echo    AI Energy Optimizer v1.0.0
echo    Smart Home Energy Management
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Starting AI Energy Optimizer...
echo.
echo The application will open in your default browser
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:8000/frontend/index.html
echo.
echo Press Ctrl+C to stop the server
echo.

python start_server.py

pause 