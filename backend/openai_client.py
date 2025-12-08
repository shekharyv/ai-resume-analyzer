"""
OpenAI API client for generating resume improvement suggestions
"""
import os
import json
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_openai_suggestions(
    resume_text: str,
    score: float,
    skills: List[str],
    years_exp: int,
    job_title: str = ""
) -> Dict:
    """
    Call OpenAI API to generate resume improvement suggestions.
    
    Args:
        resume_text: Full text of the resume
        score: Calculated resume score
        skills: List of detected skills
        years_exp: Estimated years of experience
        job_title: Optional target job title
        
    Returns:
        Dictionary with keys: suggestions (list), rewritten_bullet (str),
        title (str), ats_keywords (list)
    """
    # Truncate resume text if too long (to manage token costs)
    max_chars = 3000
    if len(resume_text) > max_chars:
        resume_text = resume_text[:max_chars] + "...[truncated]"
    
    # Build the prompt
    job_context = f" for a '{job_title}' position" if job_title else ""
    
    prompt = f"""You are an expert resume reviewer and career coach. Analyze the following resume{job_context}.

Resume Text:
{resume_text}

Current Analysis:
- Score: {score}/100
- Skills Found: {', '.join(skills) if skills else 'None detected'}
- Years of Experience: {years_exp}

Please provide actionable suggestions to improve this resume. Return your response as a JSON object with the following structure:
{{
  "suggestions": [
    "First improvement suggestion (be specific and concise)",
    "Second improvement suggestion (be specific and concise)",
    "Third improvement suggestion (be specific and concise)"
  ],
  "rewritten_bullet": "Take one bullet point from the resume and rewrite it to be more impactful with measurable achievements. If no bullet points exist, create a sample one.",
  "title": "Suggest a professional resume title or headline based on the person's experience",
  "ats_keywords": [
    "keyword1",
    "keyword2",
    "keyword3"
  ]
}}

Focus on:
1. Making achievements measurable and quantifiable
2. Using strong action verbs
3. Improving ATS compatibility
4. Highlighting relevant skills{' for ' + job_title if job_title else ''}

Return ONLY the JSON object, no additional text.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert resume reviewer. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        # Extract the response content
        content = response.choices[0].message.content.strip()
        
        # Try to parse as JSON
        try:
            suggestions_data = json.loads(content)
            
            # Validate structure
            if not isinstance(suggestions_data.get("suggestions"), list):
                raise ValueError("suggestions must be a list")
            if len(suggestions_data.get("suggestions", [])) != 3:
                # Pad or trim to exactly 3 suggestions
                suggestions_data["suggestions"] = (suggestions_data.get("suggestions", []) + ["", "", ""])[:3]
            
            if not isinstance(suggestions_data.get("ats_keywords"), list):
                suggestions_data["ats_keywords"] = []
            if len(suggestions_data.get("ats_keywords", [])) != 3:
                suggestions_data["ats_keywords"] = (suggestions_data.get("ats_keywords", []) + ["", "", ""])[:3]
            
            if "rewritten_bullet" not in suggestions_data:
                suggestions_data["rewritten_bullet"] = "No bullet point could be generated."
            
            if "title" not in suggestions_data:
                suggestions_data["title"] = "Professional"
            
            return suggestions_data
            
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw content with fallback structure
            return {
                "suggestions": [
                    "Unable to parse specific suggestions from AI",
                    "Please review the raw response below",
                    "Consider manual resume review"
                ],
                "rewritten_bullet": content[:200] if content else "No response generated",
                "title": "Professional",
                "ats_keywords": ["improvement", "needed", "review"],
                "raw": content
            }
    
    except Exception as e:
        # Return fallback suggestions if API call fails
        error_msg = str(e)
        
        return {
            "suggestions": [
                "Add more quantifiable achievements with specific metrics",
                "Use strong action verbs to begin each bullet point",
                f"Highlight relevant skills{' for ' + job_title if job_title else ''}"
            ],
            "rewritten_bullet": "Led cross-functional team of 5 to deliver project 2 weeks ahead of schedule, resulting in 15% cost savings",
            "title": f"{job_title if job_title else 'Professional'} with {years_exp}+ years of experience",
            "ats_keywords": ["achievement", "leadership", "results"],
            "error": f"OpenAI API error: {error_msg}"
        }
