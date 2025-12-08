# AI Resume Analyzer - Start Backend
Write-Host "Starting AI Resume Analyzer Backend..." -ForegroundColor Cyan
Write-Host ""

Set-Location -Path "$PSScriptRoot\backend"

if (-not (Test-Path .venv)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q fastapi "uvicorn[standard]" python-multipart pdfplumber spacy openai python-dotenv pydantic

Write-Host "Downloading spaCy model..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm

Write-Host ""
Write-Host "Starting server on http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn main:app --reload
