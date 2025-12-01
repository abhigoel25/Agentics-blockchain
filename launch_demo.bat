@echo off
REM Launch demo automatically with chatbot API

echo ========================================
echo IBM Agentics - Smart Contract Translator
echo ========================================
echo.
echo Starting chatbot API and demo...
echo.

python launch_demo.py

if errorlevel 1 (
    echo.
    echo Error starting demo. Make sure Python is installed.
    pause
)
