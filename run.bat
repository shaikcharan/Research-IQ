@echo off
setlocal enabledelayedexpansion

title ResearchIQ: Multi-Document Research Assistant
color 0B

echo ===============================================================================
echo            ResearchIQ: Multi-Document Research Assistant
echo          Evidence-Grounded RAG Platform with Hybrid Retrieval
echo ===============================================================================
echo.

REM 1. Check Python installation
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python from python.org and add it to PATH.
    pause
    exit /b 1
)

REM 2. Check Node.js installation
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not found in PATH!
    echo Please install Node.js from nodejs.org.
    pause
    exit /b 1
)

echo [1/5] Environment check passed: Python and Node.js detected.

REM 3. Create and verify storage directories
if not exist "storage\uploads" mkdir "storage\uploads"
if not exist "storage\indexes" mkdir "storage\indexes"
if not exist "storage\exports" mkdir "storage\exports"
echo [2/5] Storage directories verified.

REM 4. Setup Python dependencies
if not exist ".venv" (
    echo [3/5] Setting up Python virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo [3/5] Using existing virtual environment.
    call .venv\Scripts\activate.bat
)

REM 5. Ensure sample research PDFs exist
if not exist "storage\uploads\Solid_State_Batteries_Vance_2024.pdf" (
    echo [4/5] Generating sample research PDFs...
    python scripts\generate_sample_docs.py
) else (
    echo [4/5] Sample research PDFs ready.
)

echo [5/5] Starting ResearchIQ server at http://127.0.0.1:8000 ...
echo.
echo ===============================================================================
echo  Application is running at: http://127.0.0.1:8000
echo  FastAPI Swagger API docs: http://127.0.0.1:8000/docs
echo  Press Ctrl+C to stop the server.
echo ===============================================================================
echo.

REM Automatically open browser
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8000"

REM Launch server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
