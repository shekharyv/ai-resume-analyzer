"""
Utility functions for resume analysis
"""
import pdfplumber
import spacy
import json
import re
from typing import Dict, List, Tuple
from pathlib import Path

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

# Load skills database
SKILLS_DB_PATH = Path(__file__).parent / "skills_db.json"
with open(SKILLS_DB_PATH, 'r') as f:
    SKILLS_DATABASE = [skill.lower() for skill in json.load(f)]


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from PDF file using pdfplumber.
    
    Args:
        pdf_file: File object or path to PDF
        
    Returns:
        Extracted text as string
        
    Raises:
        ValueError: If PDF extraction fails
    """
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF. This PDF may be:\n"
                           "1. A scanned image (not searchable text)\n"
                           "2. Password protected\n"
                           "3. Corrupted or empty\n"
                           "Please try:\n"
                           "- Exporting your resume as PDF from Word/Google Docs\n"
                           "- Using a PDF with selectable text\n"
                           "- Converting scanned PDFs using OCR software")
            
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


def split_into_sections(text: str) -> Dict[str, str]:
    """
    Split resume text into sections based on common headings.
    Uses heuristic matching for section headers.
    
    Args:
        text: Raw resume text
        
    Returns:
        Dictionary mapping section names to their content
    """
    sections = {
        "contact": "",
        "summary": "",
        "experience": "",
        "education": "",
        "skills": "",
        "projects": "",
        "other": ""
    }
    
    # Common section header patterns
    section_patterns = {
        "experience": r"(?i)(work\s+)?experience|employment\s+history|professional\s+experience",
        "education": r"(?i)education|academic\s+background|qualifications",
        "skills": r"(?i)(technical\s+)?skills|competencies|expertise",
        "projects": r"(?i)projects|portfolio",
        "summary": r"(?i)summary|profile|objective|about\s+me",
        "contact": r"(?i)contact|personal\s+information"
    }
    
    lines = text.split('\n')
    current_section = "other"
    
    for line in lines:
        line_stripped = line.strip()
        
        # Check if this line is a section header
        is_header = False
        for section_name, pattern in section_patterns.items():
            if re.match(pattern, line_stripped) and len(line_stripped) < 50:
                current_section = section_name
                is_header = True
                break
        
        # Add content to current section (skip the header line itself)
        if not is_header and line_stripped:
            sections[current_section] += line + "\n"
    
    return sections


def extract_skills(text: str, sections: Dict[str, str]) -> List[str]:
    """
    Extract skills from resume using spaCy NLP and skills database matching.
    Supports multi-word skills.
    
    Args:
        text: Full resume text
        sections: Dictionary of resume sections
        
    Returns:
        List of unique skills found
    """
    found_skills = set()
    
    # Combine relevant sections for skill searching
    search_text = (
        sections.get("skills", "") + " " + 
        sections.get("experience", "") + " " + 
        sections.get("projects", "")
    ).lower()
    
    # Also search full text as fallback
    full_text_lower = text.lower()
    
    # Method 1: Direct string matching (handles multi-word skills)
    for skill in SKILLS_DATABASE:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, search_text) or re.search(pattern, full_text_lower):
            found_skills.add(skill)
    
    # Method 2: Use spaCy for entity and token extraction (if available)
    if nlp:
        doc = nlp(search_text[:10000])  # Limit text length for performance
        
        # Extract noun chunks and tokens
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower().strip()
            if chunk_text in SKILLS_DATABASE:
                found_skills.add(chunk_text)
        
        for token in doc:
            token_text = token.text.lower()
            if token_text in SKILLS_DATABASE:
                found_skills.add(token_text)
    
    return sorted(list(found_skills))


def estimate_years_of_experience(text: str, sections: Dict[str, str]) -> int:
    """
    Estimate years of experience using heuristics:
    1. Look for explicit mentions like "5 years of experience"
    2. Parse date ranges in experience section (2018-2021, Jan 2019 - Dec 2020)
    3. Count distinct years mentioned
    
    Args:
        text: Full resume text
        sections: Dictionary of resume sections
        
    Returns:
        Estimated years of experience as integer
    """
    experience_text = sections.get("experience", "") + " " + text
    
    # Pattern 1: Explicit years mention (e.g., "5 years of experience")
    explicit_pattern = r'(\d+)\+?\s*years?\s+(?:of\s+)?(?:experience|exp)'
    explicit_matches = re.findall(explicit_pattern, experience_text, re.IGNORECASE)
    if explicit_matches:
        return max(int(match) for match in explicit_matches)
    
    # Pattern 2: Date ranges
    total_months = 0
    
    # Match patterns like "2018-2021", "2018 - 2021", "Jan 2018 - Dec 2020"
    date_range_patterns = [
        r'(\d{4})\s*[-–—]\s*(\d{4})',  # 2018-2021
        r'(\d{4})\s*[-–—]\s*(?:present|current)',  # 2018-Present
        r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+(\d{4})\s*[-–—]\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+(\d{4})',  # Jan 2018 - Dec 2020
    ]
    
    from datetime import datetime
    current_year = datetime.now().year
    
    for pattern in date_range_patterns:
        matches = re.findall(pattern, experience_text, re.IGNORECASE)
        for match in matches:
            if len(match) == 2:
                try:
                    start_year = int(match[0])
                    end_year = int(match[1]) if match[1].isdigit() else current_year
                    
                    # Sanity check
                    if 1980 <= start_year <= current_year and start_year <= end_year <= current_year + 1:
                        total_months += (end_year - start_year) * 12
                except ValueError:
                    continue
    
    if total_months > 0:
        return max(1, round(total_months / 12))
    
    # Pattern 3: Fallback - count distinct years mentioned
    year_pattern = r'\b(19\d{2}|20\d{2})\b'
    years = set(re.findall(year_pattern, experience_text))
    years = [int(y) for y in years if 1980 <= int(y) <= current_year]
    
    if years:
        return max(1, current_year - min(years))
    
    # Default fallback
    return 0


def calculate_score(
    text: str,
    sections: Dict[str, str],
    skills: List[str],
    years_exp: int,
    job_title: str = ""
) -> Tuple[float, Dict[str, float]]:
    """
    Calculate resume score based on rubric:
    - Experience: 30 points
    - Skills: 35 points
    - Education: 15 points
    - Format: 10 points
    - Keywords: 10 points
    
    Args:
        text: Full resume text
        sections: Dictionary of sections
        skills: List of extracted skills
        years_exp: Years of experience
        job_title: Optional job title for keyword matching
        
    Returns:
        Tuple of (total_score, breakdown_dict)
    """
    breakdown = {
        "experience": 0.0,
        "skills": 0.0,
        "education": 0.0,
        "format": 0.0,
        "keywords": 0.0
    }
    
    # Experience scoring (0-30 points)
    # 0-2 years: 0-15, 3-5 years: 16-25, 6+ years: 26-30
    if years_exp >= 6:
        breakdown["experience"] = 30.0
    elif years_exp >= 3:
        breakdown["experience"] = 15.0 + (years_exp - 3) * 3.3
    else:
        breakdown["experience"] = years_exp * 7.5
    
    breakdown["experience"] = min(30.0, breakdown["experience"])
    
    # Skills scoring (0-35 points)
    # Based on number of skills: 0-5 skills: 0-15, 6-10: 16-25, 11+: 26-35
    skill_count = len(skills)
    if skill_count >= 11:
        breakdown["skills"] = 35.0
    elif skill_count >= 6:
        breakdown["skills"] = 15.0 + (skill_count - 6) * 2.0
    else:
        breakdown["skills"] = skill_count * 3.0
    
    breakdown["skills"] = min(35.0, breakdown["skills"])
    
    # Education scoring (0-15 points)
    education_text = sections.get("education", "").lower()
    edu_score = 0.0
    
    if any(word in education_text for word in ["phd", "ph.d", "doctorate"]):
        edu_score = 15.0
    elif any(word in education_text for word in ["master", "msc", "mba", "m.s", "m.a"]):
        edu_score = 12.0
    elif any(word in education_text for word in ["bachelor", "bsc", "ba", "b.s", "b.a", "undergraduate"]):
        edu_score = 10.0
    elif any(word in education_text for word in ["associate", "diploma", "certification"]):
        edu_score = 7.0
    elif education_text.strip():
        edu_score = 5.0
    
    breakdown["education"] = edu_score
    
    # Format scoring (0-10 points)
    format_score = 0.0
    
    # Check for contact information
    if sections.get("contact") or re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text):
        format_score += 2.0
    
    # Check for bullet points or structured content
    if text.count('•') > 3 or text.count('-') > 5:
        format_score += 2.0
    
    # Check for multiple sections
    non_empty_sections = sum(1 for s in sections.values() if s.strip())
    if non_empty_sections >= 4:
        format_score += 3.0
    elif non_empty_sections >= 2:
        format_score += 1.5
    
    # Check length (not too short, not too long)
    word_count = len(text.split())
    if 300 <= word_count <= 1500:
        format_score += 3.0
    elif 150 <= word_count <= 2000:
        format_score += 1.5
    
    breakdown["format"] = min(10.0, format_score)
    
    # Keywords scoring (0-10 points)
    # Check for ATS-friendly keywords based on job title
    keyword_score = 0.0
    text_lower = text.lower()
    
    # Common ATS keywords
    ats_keywords = [
        "achieved", "improved", "increased", "reduced", "managed", "led",
        "developed", "implemented", "designed", "analyzed", "created",
        "results", "metrics", "team", "project", "delivered"
    ]
    
    keyword_matches = sum(1 for kw in ats_keywords if kw in text_lower)
    keyword_score = min(10.0, keyword_matches * 0.7)
    
    breakdown["keywords"] = keyword_score
    
    # Calculate total
    total = sum(breakdown.values())
    
    # Round breakdown values
    breakdown = {k: round(v, 2) for k, v in breakdown.items()}
    
    return round(total, 2), breakdown
