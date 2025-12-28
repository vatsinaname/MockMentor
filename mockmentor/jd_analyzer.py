"""
JD Analyzer
Extracts structured requirements from job descriptions using LLM
"""

import json
from typing import Optional


def parse_jd_with_llm(jd_text: str) -> dict:
    """
    Use LLM to extract structured information from job description.
    
    Returns:
        {
            "title": str,
            "company": str,
            "required_skills": [str],
            "preferred_skills": [str],
            "experience_required": {"min": int, "max": int},
            "education_required": str,
            "responsibilities": [str],
            "key_competencies": [str],
            "interview_topics": [str],
            "summary": str
        }
    """
    from .tools import get_eval_model
    
    model = get_eval_model()
    
    prompt = f"""
    Extract structured information from this job description. Return ONLY valid JSON.
    
    Job Description:
    {jd_text[:8000]}
    
    Return JSON with this exact structure:
    {{
        "title": "Job Title",
        "company": "Company Name or null",
        "required_skills": ["must-have skill 1", "must-have skill 2"],
        "preferred_skills": ["nice-to-have skill 1"],
        "experience_required": {{"min": 2, "max": 5}},
        "education_required": "Bachelor's in CS or equivalent",
        "responsibilities": ["responsibility 1", "responsibility 2"],
        "key_competencies": ["competency that would be tested in interview"],
        "interview_topics": [
            "Topic 1 that interviewer would likely ask about",
            "Topic 2",
            "Topic 3"
        ],
        "summary": "Brief 1-2 sentence summary of the role"
    }}
    
    For interview_topics, think about what an interviewer would realistically ask 
    based on this JD. Include both technical and behavioral topics.
    
    Return ONLY the JSON, no markdown.
    """
    
    try:
        response = model.generate(prompt)
        text = response.text.strip()
        
        # Clean up potential markdown formatting
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()
        
        return json.loads(text)
    except Exception as e:
        return {
            "title": "Unknown Role",
            "company": None,
            "required_skills": [],
            "preferred_skills": [],
            "experience_required": {"min": 0, "max": 0},
            "education_required": None,
            "responsibilities": [],
            "key_competencies": [],
            "interview_topics": [],
            "summary": f"Failed to parse JD: {str(e)}",
            "raw_text": jd_text[:2000]
        }


def analyze_jd(jd_text: str) -> dict:
    """
    Main entry point for JD analysis.
    
    Args:
        jd_text: Raw job description text
    
    Returns:
        Structured JD data dict
    """
    parsed = parse_jd_with_llm(jd_text)
    parsed["raw_text"] = jd_text
    return parsed
