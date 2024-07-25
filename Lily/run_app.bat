@echo off

REM Run the Flask application
py "C:\Users\ksame\Desktop\Lily\app.py"

echo hello
REM Wait for a few seconds to ensure the server starts
timeout /t 3 /nobreak

REM Open the default web browser to the Flask app's URL
start http://127.0.0.1:5000/

REM Keep the command prompt window open (optional)
pause
