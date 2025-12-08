@echo off
echo Starting AI Resume Analyzer Frontend...
echo.

cd /d "%~dp0frontend"

if not exist node_modules (
    echo Installing dependencies...
    call npm install
)

echo.
echo Starting development server...
echo.
call npm run dev

pause
