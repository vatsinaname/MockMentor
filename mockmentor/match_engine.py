"""
Match Engine
Calculates match score between resume and job description
"""

import json
from typing import List, Dict


def calculate_skill_match(resume_skills: List[str], jd_required: List[str], jd_preferred: List[str]) -> dict:
    """
    Calculate skill matching metrics.
    
    Returns:
        {
            "required_match_pct": float (0-100),
            "preferred_match_pct": float (0-100),
            "matched_required": [str],
            "matched_preferred": [str],
            "missing_required": [str],
            "missing_preferred": [str]
        }
    """
    # Normalize skills for comparison
    resume_skills_lower = set(s.lower().strip() for s in resume_skills)
    jd_required_lower = {s.lower().strip(): s for s in jd_required}
    jd_preferred_lower = {s.lower().strip(): s for s in jd_preferred}
    
    matched_required = []
    missing_required = []
    
    for skill_lower, skill_orig in jd_required_lower.items():
        # Check for exact or partial match
        if skill_lower in resume_skills_lower or any(skill_lower in rs for rs in resume_skills_lower):
            matched_required.append(skill_orig)
        else:
            missing_required.append(skill_orig)
    
    matched_preferred = []
    missing_preferred = []
    
    for skill_lower, skill_orig in jd_preferred_lower.items():
        if skill_lower in resume_skills_lower or any(skill_lower in rs for rs in resume_skills_lower):
            matched_preferred.append(skill_orig)
        else:
            missing_preferred.append(skill_orig)
    
    required_pct = (len(matched_required) / len(jd_required) * 100) if jd_required else 100
    preferred_pct = (len(matched_preferred) / len(jd_preferred) * 100) if jd_preferred else 100
    
    return {
        "required_match_pct": round(required_pct, 1),
        "preferred_match_pct": round(preferred_pct, 1),
        "matched_required": matched_required,
        "matched_preferred": matched_preferred,
        "missing_required": missing_required,
        "missing_preferred": missing_preferred
    }


def calculate_experience_match(resume_years: float, required: dict) -> dict:
    """
    Calculate experience level match.
    
    Args:
        resume_years: Years of experience from resume
        required: {"min": int, "max": int} from JD
    
    Returns:
        {"match_pct": float, "status": str, "gap": str}
    """
    min_years = required.get("min", 0)
    max_years = required.get("max", 99)
    
    if resume_years >= min_years:
        if resume_years <= max_years:
            return {"match_pct": 100, "status": "ideal", "gap": None}
        else:
            return {"match_pct": 90, "status": "overqualified", "gap": f"{resume_years - max_years} years over"}
    else:
        gap = min_years - resume_years
        pct = (resume_years / min_years * 100) if min_years > 0 else 0
        return {"match_pct": round(pct, 1), "status": "underqualified", "gap": f"{gap} years short"}


def calculate_overall_match(resume: dict, jd: dict) -> dict:
    """
    Calculate comprehensive match score.
    
    Args:
        resume: Parsed resume dict
        jd: Parsed JD dict
    
    Returns:
        {
            "overall_score": float (0-100),
            "skill_match": {...},
            "experience_match": {...},
            "strengths": [str],
            "gaps": [str],
            "interview_focus_areas": [str],
            "recommendation": str
        }
    """
    # Skill matching
    skill_match = calculate_skill_match(
        resume.get("skills", []),
        jd.get("required_skills", []),
        jd.get("preferred_skills", [])
    )
    
    # Experience matching
    exp_match = calculate_experience_match(
        resume.get("experience_years", 0),
        jd.get("experience_required", {"min": 0, "max": 99})
    )
    
    # Calculate weighted overall score
    # 60% required skills, 20% preferred skills, 20% experience
    overall = (
        skill_match["required_match_pct"] * 0.6 +
        skill_match["preferred_match_pct"] * 0.2 +
        exp_match["match_pct"] * 0.2
    )
    
    # Identify strengths
    strengths = skill_match["matched_required"][:5]
    
    # Identify gaps for interview focus
    gaps = skill_match["missing_required"][:5]
    
    # Combine JD interview topics with identified gaps
    interview_focus = list(set(
        jd.get("interview_topics", [])[:5] + 
        skill_match["missing_required"][:3]
    ))
    
    # Generate recommendation
    if overall >= 80:
        rec = "Strong match! Focus on demonstrating depth in your strengths."
    elif overall >= 60:
        rec = "Good match with some gaps. Prepare to address missing skills."
    elif overall >= 40:
        rec = "Moderate match. Focus heavily on transferable skills."
    else:
        rec = "Consider upskilling in key areas before applying."
    
    return {
        "overall_score": round(overall, 1),
        "skill_match": skill_match,
        "experience_match": exp_match,
        "strengths": strengths,
        "gaps": gaps,
        "interview_focus_areas": interview_focus,
        "recommendation": rec
    }


def analyze_match(resume: dict, jd: dict) -> dict:
    """
    Main entry point for match analysis.
    
    Args:
        resume: Parsed resume from resume_parser
        jd: Parsed JD from jd_analyzer
    
    Returns:
        Complete match analysis dict
    """
    match_result = calculate_overall_match(resume, jd)
    
    # Add metadata
    match_result["resume_name"] = resume.get("name", "Candidate")
    match_result["job_title"] = jd.get("title", "Position")
    match_result["company"] = jd.get("company")
    
    return match_result
