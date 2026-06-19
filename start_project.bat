@echo off

start cmd /k "cd /d C:\diseaseprediction\backend && uvicorn app.main:app --reload"

timeout /t 3 > nul

start cmd /k "cd /d C:\diseaseprediction\frontend && npm run dev"