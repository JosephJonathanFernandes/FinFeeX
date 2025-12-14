# FinFeeX Quick Launch Script for PowerShell

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FinFeeX - Hidden-Fees X-Ray" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path ".venv")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: make install" -ForegroundColor Yellow
    Write-Host "Or: python -m venv .venv" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Blue
& .\.venv\Scripts\Activate.ps1

# Run the app
Write-Host "[INFO] Starting Streamlit app..." -ForegroundColor Blue
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  App will open in your browser" -ForegroundColor Green
Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

streamlit run app.py
