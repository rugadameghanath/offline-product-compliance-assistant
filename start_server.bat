@echo off
set PYTHONIOENCODING=utf-8
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"
echo Starting OPCA web server...
start python server.py
timeout /t 3 >nul
start http://localhost:5000
echo Server running. Close this window to stop.