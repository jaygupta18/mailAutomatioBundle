@echo off
echo Starting Gmail AI Assistant Server...
echo.
echo Make sure you have:
echo 1. Python installed
echo 2. Dependencies installed (pip install -r requirements.txt)
echo 3. credentials.json file in the same directory
echo 4. Valid API key in openai_reply.py
echo.
echo Press any key to continue...
pause >nul

echo.
echo Starting server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python server.py

echo.
echo Server stopped.
pause 