@echo off
REM FinFeeX Quick Launch Script for Windows

echo.
echo ========================================
echo   FinFeeX - Hidden-Fees X-Ray
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run: make install
    echo Or: python -m venv .venv
    pause
    exit /b 1
)

REM Activate virtual environment and run app
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [INFO] Starting Streamlit app...
echo.
echo ========================================
echo   App will open in your browser
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

streamlit run app.py

pause
