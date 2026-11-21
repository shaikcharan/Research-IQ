@echo off
setlocal enabledelayedexpansion

title ResearchIQ: Initial Environment Setup
color 0A

echo ===============================================================================
echo                ResearchIQ: Environment Setup Wizard
echo ===============================================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found in PATH!
    pause
    exit /b 1
)

where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found in PATH!
    pause
    exit /b 1
)

if not exist "storage\uploads" mkdir "storage\uploads"
if not exist "storage\indexes" mkdir "storage\indexes"
if not exist "storage\exports" mkdir "storage\exports"

echo [1/4] Setting up Python virtual environment...
if not exist ".venv" python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [2/4] Setting up React frontend...
cd frontend
call npm install
call npm run build
cd ..

echo [3/4] Generating academic research papers...
python scripts\generate_sample_docs.py

echo [4/4] Running automated test verification...
python -m pytest backend\tests\ -q

echo.
echo ===============================================================================
echo  Setup Completed Successfully!
echo  You can now start the application anytime by running: run.bat
echo ===============================================================================
pause
