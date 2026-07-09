@echo off

cd /d "%~dp0"

start "Disease Backend" cmd /k "cd /d "%~dp0backend" && "%~dp0venv\Scripts\python.exe" -m uvicorn app.main:app --reload"

timeout /t 3 > nul

start "Disease Frontend" cmd /k "cd /d "%~dp0frontend" && npm.cmd run dev"
