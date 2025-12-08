# AI Resume Analyzer - Backend

FastAPI backend for analyzing resumes with AI-powered insights.

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate Virtual Environment

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
.venv\Scripts\activate.bat
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### 5. Configure Environment Variables

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env` and replace `your_openai_api_key_here` with your actual OpenAI API key.

**Important:** Never commit your `.env` file to version control!

### 6. Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing the API

### Using cURL (Windows PowerShell)

Create a test PDF file first, then:

```powershell
curl -X POST "http://localhost:8000/analyze" `
  -F "file=@C:\path\to\your\resume.pdf" `
  -F "job_title=Software Engineer"
```

### Using cURL (Mac/Linux)

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@/path/to/your/resume.pdf" \
  -F "job_title=Software Engineer"
```

### Expected Response

```json
{
  "score": 75.5,
  "breakdown": {
    "experience": 25.0,
    "skills": 30.0,
    "education": 10.0,
    "format": 8.5,
    "keywords": 2.0
  },
  "skills": ["python", "react", "docker", "aws"],
  "years_experience": 5,
  "suggestions": {
    "suggestions": [
      "Add more quantifiable achievements",
      "Include specific technologies used",
      "Expand on leadership experience"
    ],
    "rewritten_bullet": "Led team of 5 engineers to deliver customer portal, increasing user engagement by 40%",
    "title": "Senior Full-Stack Software Engineer",
    "ats_keywords": ["agile", "microservices", "ci/cd"]
  },
  "raw_text_preview": "..."
}
```

## CORS Configuration

By default, the backend allows requests from `http://localhost:5173` (Vite's default port). To modify this, set the `FRONTEND_URL` environment variable in your `.env` file.

## Privacy & Security

- Uploaded files are processed in-memory and not saved to disk (unless `store=true` is passed)
- No resume data is persisted in the database
- OpenAI API calls are made over HTTPS
- Be mindful of OpenAI API costs and rate limits

## Troubleshooting

### Import errors

Make sure you've activated the virtual environment and installed all dependencies.

### spaCy model not found

Run `python -m spacy download en_core_web_sm`

### OpenAI API errors

- Check your API key is correct in `.env`
- Verify you have available credits in your OpenAI account
- Check rate limits if getting 429 errors
