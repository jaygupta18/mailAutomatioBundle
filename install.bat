@echo off
echo ========================================
echo Gmail AI Assistant - Installation Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo Next steps:
echo 1. Make sure you have credentials.json in this directory
echo 2. Update your API key in openai_reply.py
echo 3. Run start_server.bat to start the server
echo 4. Load the extension in Chrome
echo.
echo Installation complete!
pause 