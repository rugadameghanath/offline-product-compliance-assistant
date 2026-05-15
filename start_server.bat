@echo off
cd /d D:\GitPros\OPCA
echo Starting OPCA web server...
start python server.py
timeout /t 3
start http://localhost:5000
echo Server running. Close this window to stop.