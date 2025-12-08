# AI Resume Analyzer

A full-stack AI-powered resume analysis tool that provides instant feedback, scoring, and actionable suggestions to improve your resume.

## Features

- **PDF Resume Upload**: Simple drag-and-drop interface for PDF resumes
- **Comprehensive Scoring**: 0-100 score with detailed breakdown across 5 categories:
  - Experience (30 points)
  - Skills (35 points)
  - Education (15 points)
  - Format (10 points)
  - ATS Keywords (10 points)
- **Skills Detection**: Automatically identifies technical and professional skills
- **Experience Estimation**: Calculates years of experience from resume content
- **AI-Powered Suggestions**: Uses OpenAI GPT to provide:
  - 3 specific improvement recommendations
  - Rewritten bullet point with measurable achievements
  - Suggested professional resume title
  - 3 ATS-friendly keywords to include
- **Real-time Analysis**: Get results in seconds
- **Privacy-First**: Resumes are processed in-memory and not stored

## Tech Stack

### Backend

- **Framework**: FastAPI (Python 3.9+)
- **PDF Processing**: pdfplumber
- **NLP**: spaCy (en_core_web_sm model)
- **AI**: OpenAI API (GPT-3.5)
- **Server**: Uvicorn

### Frontend

- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Native Fetch API

## Project Structure

```
ai-resume-analyzer/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── utils.py                # PDF parsing, skills extraction, scoring
│   ├── openai_client.py        # OpenAI API integration
│   ├── skills_db.json          # Skills database
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── README.md               # Backend documentation
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── api.js             # API client
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Tailwind styles
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   └── README.md              # Frontend documentation
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- **Python 3.9+** (backend)
- **Node.js 18+** and npm (frontend)
- **OpenAI API Key** (get one at https://platform.openai.com/api-keys)

### Backend Setup

1. **Navigate to backend directory**

   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**

   Windows (PowerShell):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Mac/Linux:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model**

   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Configure environment variables**

   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=your_actual_api_key_here
   ```

6. **Run the backend server**

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`

   - API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Run the development server**

   ```bash
   npm run dev
   ```

   The application will open at `http://localhost:5173`

### Running the Complete Application

1. **Terminal 1** - Start backend:

   ```bash
   cd backend
   .\.venv\Scripts\Activate.ps1  # Windows
   uvicorn main:app --reload
   ```

2. **Terminal 2** - Start frontend:

   ```bash
   cd frontend
   npm run dev
   ```

3. **Open browser** to `http://localhost:5173`

## How It Works

### Scoring Methodology

The resume analyzer uses a comprehensive rubric to evaluate resumes:

1. **Experience (30 points)**

   - Based on years of experience detected
   - Analyzes work history patterns and date ranges
   - 0-2 years: 0-15 points
   - 3-5 years: 16-25 points
   - 6+ years: 26-30 points

2. **Skills (35 points)**

   - Matches against database of 70+ common technical skills
   - Uses spaCy NLP for intelligent skill extraction
   - 0-5 skills: 0-15 points
   - 6-10 skills: 16-25 points
   - 11+ skills: 26-35 points

3. **Education (15 points)**

   - Detects degree levels and certifications
   - PhD/Doctorate: 15 points
   - Master's: 12 points
   - Bachelor's: 10 points
   - Associate/Diploma: 7 points

4. **Format (10 points)**

   - Contact information presence
   - Structure and organization
   - Appropriate length (300-1500 words)
   - Use of bullet points

5. **Keywords (10 points)**
   - ATS-friendly action verbs
   - Industry-standard terminology
   - Results-oriented language

### AI Suggestions

The application uses OpenAI's GPT-3.5 model to provide personalized recommendations:

- Analyzes your resume content and score
- Provides 3 specific, actionable improvements
- Rewrites a bullet point to be more impactful
- Suggests a professional headline
- Recommends ATS keywords relevant to your field

## Privacy & Security

- **No Storage**: Resume files are processed in-memory and immediately discarded
- **No Database**: No personal information is stored
- **Secure Transmission**: All API calls use HTTPS
- **OpenAI Privacy**: Resume content is sent to OpenAI API for analysis (see OpenAI's privacy policy)

## API Costs & Rate Limits

- This application uses OpenAI's GPT-3.5-turbo model
- Each resume analysis costs approximately $0.01-0.02
- Be mindful of OpenAI rate limits on free tier accounts
- Monitor your usage at https://platform.openai.com/usage

## Testing

### Manual Testing with cURL

**Windows PowerShell:**

```powershell
curl -X POST "http://localhost:8000/analyze" `
  -F "file=@C:\path\to\resume.pdf" `
  -F "job_title=Software Engineer"
```

**Mac/Linux:**

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@/path/to/resume.pdf" \
  -F "job_title=Software Engineer"
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Troubleshooting

### Backend Issues

**spaCy model not found**

```bash
python -m spacy download en_core_web_sm
```

**OpenAI API errors**

- Verify your API key in `.env`
- Check you have available credits
- Monitor rate limits at https://platform.openai.com/account/rate-limits

**PDF extraction fails**

- Ensure PDF contains selectable text (not scanned images)
- Try re-saving the PDF from Word or another editor
- Check PDF is not password-protected

### Frontend Issues

**Cannot connect to backend**

- Verify backend is running on `http://localhost:8000`
- Check CORS settings in `backend/main.py`
- Clear browser cache

**File upload fails**

- Ensure file is PDF format
- Check file size (backend may have limits)
- Try a different PDF file

## Development

### Adding New Skills

Edit `backend/skills_db.json` and add skills to the array:

```json
["python", "react", "your_new_skill"]
```

### Customizing Scoring

Modify the `calculate_score` function in `backend/utils.py` to adjust the scoring rubric.

### Changing AI Model

Edit `backend/openai_client.py` to use a different OpenAI model (e.g., `gpt-4`):

```python
model="gpt-4"  # More accurate but more expensive
```

## Building for Production

### Backend

```bash
# Set production environment variables
export OPENAI_API_KEY=your_key
export PORT=8000

# Run with production server
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

```bash
cd frontend
npm run build
npm run preview  # Test production build
```

Deploy the `dist` folder to your hosting service (Vercel, Netlify, etc.)

## Contributing

This is an MVP project. Potential improvements:

- [ ] Support for Word documents (.docx)
- [ ] Resume comparison feature
- [ ] Multiple AI model options
- [ ] Job description matching score
- [ ] Resume templates and suggestions
- [ ] Export analysis as PDF report
- [ ] User accounts and history
- [ ] Batch processing
- [ ] Resume ATS scan simulation

## License

This project is provided as-is for educational and personal use.

## Acknowledgments

- OpenAI for GPT API
- spaCy for NLP capabilities
- FastAPI for the excellent Python framework
- React and Vite teams for modern frontend tools

## Support

For issues or questions:

1. Check the documentation in `backend/README.md` and `frontend/README.md`
2. Review the troubleshooting section above
3. Ensure all dependencies are correctly installed
4. Verify your OpenAI API key is valid and has credits

---

**Note**: This is an MVP (Minimum Viable Product). Always review AI suggestions critically and consult with career professionals for important decisions.
