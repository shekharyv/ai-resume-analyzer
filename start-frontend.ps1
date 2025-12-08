# AI Resume Analyzer - Start Frontend
Write-Host "Starting AI Resume Analyzer Frontend..." -ForegroundColor Cyan
Write-Host ""

Set-Location -Path "$PSScriptRoot\frontend"

if (-not (Test-Path node_modules)) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host ""
Write-Host "Starting development server..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

npm run dev
