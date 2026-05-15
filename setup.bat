@echo off
title OPCA Environment Setup
echo =======================================
echo Offline Product & Compliance Assistant
echo =======================================
echo.

REM 1. Check Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo     Python found.
echo.

REM 2. Install Python dependencies
echo [2/4] Installing Python packages from requirements.txt...
if not exist requirements.txt (
    echo requirements.txt not found. Please ensure it exists.
    pause
    exit /b 1
)
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install packages. Try running as Administrator.
    pause
    exit /b 1
)
echo     Packages installed.
echo.

REM 3. Check Ollama
echo [3/4] Checking Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama is not installed or not in PATH.
    echo Please download and install Ollama from https://ollama.com
    echo After installation, re-run this script.
    pause
    exit /b 1
)
echo     Ollama found.
echo.

REM 4. Pull the LLM model
echo [4/4] Pulling LLM model (llama3.2:3b)...
echo This will take a few minutes depending on your internet speed.
ollama pull llama3.2:3b
if %errorlevel% neq 0 (
    echo Failed to pull model. Check your internet connection.
    pause
    exit /b 1
)
echo     Model downloaded.
echo.

echo =======================================
echo Setup completed successfully!
echo You can now run start_server.bat
echo =======================================
pause