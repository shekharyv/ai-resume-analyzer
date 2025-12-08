@echo off
echo Starting AI Resume Analyzer Backend...
echo.

cd /d "%~dp0backend"

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install -q fastapi uvicorn[standard] python-multipart pdfplumber spacy openai python-dotenv pydantic

echo Downloading spaCy model...
python -m spacy download en_core_web_sm

echo.
echo Starting server on http://localhost:8000
echo.
python -m uvicorn main:app --reload

pause
