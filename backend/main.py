"""
AI Resume Analyzer - FastAPI Backend
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import hashlib
import os
from dotenv import load_dotenv

from utils import (
    extract_text_from_pdf,
    split_into_sections,
    extract_skills,
    estimate_years_of_experience,
    calculate_score
)
from openai_client import call_openai_suggestions

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Analyzer",
    description="Analyze resumes with AI-powered insights and scoring",
    version="1.0.0"
)

# CORS configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cache for analysis results (optional feature)
# Key: file content hash, Value: analysis result
analysis_cache: Dict[str, dict] = {}


# Response models
class AnalysisBreakdown(BaseModel):
    experience: float
    skills: float
    education: float
    format: float
    keywords: float


class SuggestionsData(BaseModel):
    suggestions: List[str]
    rewritten_bullet: str
    title: str
    ats_keywords: List[str]


class AnalysisResponse(BaseModel):
    score: float
    breakdown: AnalysisBreakdown
    skills: List[str]
    years_experience: int
    suggestions: Dict
    raw_text_preview: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Resume Analyzer API",
        "status": "running",
        "docs": "/docs"
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    file: UploadFile = File(..., description="PDF resume file to analyze"),
    job_title: Optional[str] = Form(None, description="Target job title (optional)"),
    store: bool = Form(False, description="Whether to store the file (not implemented in MVP)")
):
    """
    Analyze a resume PDF and return comprehensive insights.
    
    Returns:
    - score: Overall score (0-100)
    - breakdown: Score breakdown by category
    - skills: List of detected skills
    - years_experience: Estimated years of experience
    - suggestions: AI-generated improvement suggestions
    - raw_text_preview: First 1000 characters of extracted text
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted. Please upload a .pdf file."
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Calculate content hash for caching
        content_hash = hashlib.md5(file_content).hexdigest()
        
        # Check cache
        if content_hash in analysis_cache:
            cached_result = analysis_cache[content_hash]
            return {**cached_result, "cached": True}
        
        # Extract text from PDF
        try:
            # Create a temporary file-like object
            from io import BytesIO
            pdf_file = BytesIO(file_content)
            text = extract_text_from_pdf(pdf_file)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="The PDF appears to be empty or contains no extractable text. Please ensure the PDF contains readable text."
            )
        
        # Split into sections
        sections = split_into_sections(text)
        
        # Extract skills
        skills = extract_skills(text, sections)
        
        # Estimate years of experience
        years_exp = estimate_years_of_experience(text, sections)
        
        # Calculate score
        score, breakdown = calculate_score(
            text=text,
            sections=sections,
            skills=skills,
            years_exp=years_exp,
            job_title=job_title or ""
        )
        
        # Get AI-powered suggestions
        try:
            suggestions = call_openai_suggestions(
                resume_text=text,
                score=score,
                skills=skills,
                years_exp=years_exp,
                job_title=job_title or ""
            )
        except Exception as e:
            # Fallback suggestions if OpenAI fails
            suggestions = {
                "suggestions": [
                    "Add quantifiable achievements with specific metrics",
                    "Use strong action verbs to begin bullet points",
                    "Ensure all relevant skills are clearly listed"
                ],
                "rewritten_bullet": "Led team of 5 to deliver project ahead of schedule, reducing costs by 15%",
                "title": f"Experienced Professional with {years_exp}+ years",
                "ats_keywords": ["achievement", "leadership", "results"],
                "error": f"AI suggestions unavailable: {str(e)}"
            }
        
        # Prepare response
        result = {
            "score": score,
            "breakdown": breakdown,
            "skills": skills,
            "years_experience": years_exp,
            "suggestions": suggestions,
            "raw_text_preview": text[:1000]
        }
        
        # Cache the result
        analysis_cache[content_hash] = result
        
        # Note about storage
        if store:
            result["storage_note"] = "File storage not implemented in this MVP version. Resumes are processed in-memory only."
        
        return result
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while analyzing the resume: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Detailed health check"""
    import spacy
    
    checks = {
        "api": "healthy",
        "spacy_model": "not loaded",
        "openai_key": "not configured"
    }
    
    # Check spaCy
    try:
        nlp = spacy.load("en_core_web_sm")
        checks["spacy_model"] = "loaded"
    except:
        checks["spacy_model"] = "missing - run: python -m spacy download en_core_web_sm"
    
    # Check OpenAI key
    if os.getenv("OPENAI_API_KEY"):
        checks["openai_key"] = "configured"
    else:
        checks["openai_key"] = "missing - add OPENAI_API_KEY to .env"
    
    return checks


@app.get("/stats")
async def get_stats():
    """Get API statistics"""
    return {
        "cached_analyses": len(analysis_cache),
        "cache_size_kb": sum(
            len(str(v)) for v in analysis_cache.values()
        ) / 1024
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
