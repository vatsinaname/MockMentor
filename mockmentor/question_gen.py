"""
Dynamic Question Generator
Generates personalized interview questions based on JD, resume, and match analysis
"""

import json
import random
from typing import List, Dict, Optional


def generate_interview_plan(jd: dict, resume: dict, match: dict, num_questions: int = 15) -> dict:
    """
    Create a personalized interview plan with dynamically generated questions.
    
    Args:
        jd: Parsed job description
        resume: Parsed resume
        match: Match analysis result
        num_questions: Total questions for the session
    
    Returns:
        {
            "topics": [{"name": str, "weight": float, "questions_allocated": int}],
            "questions": [{"topic": str, "text": str, "difficulty": str, "type": str}],
            "focus_areas": [str]
        }
    """
    from .tools import get_eval_model
    
    model = get_eval_model()
    
    # Build context for question generation
    context = f"""
    Job Title: {jd.get('title', 'Unknown')}
    Company: {jd.get('company', 'Unknown')}
    
    Required Skills: {', '.join(jd.get('required_skills', [])[:10])}
    Key Responsibilities: {', '.join(jd.get('responsibilities', [])[:5])}
    Interview Topics from JD: {', '.join(jd.get('interview_topics', [])[:5])}
    
    Candidate Strengths: {', '.join(match.get('strengths', [])[:5])}
    Candidate Gaps: {', '.join(match.get('gaps', [])[:5])}
    Experience: {resume.get('experience_years', 0)} years
    Candidate Skills: {', '.join(resume.get('skills', [])[:10])}
    """
    
    prompt = f"""
    You are creating a personalized mock interview for a candidate.
    
    Context:
    {context}
    
    Generate exactly {num_questions} interview questions. Mix of:
    - Technical questions (60%) - test required skills
    - Behavioral questions (25%) - STAR format situations  
    - Case/scenario questions (15%) - real-world problems
    
    For technical questions, focus MORE on the candidate's GAPS to help them prepare.
    Include some questions on their STRENGTHS to build confidence.
    
    Return ONLY valid JSON array:
    [
        {{
            "topic": "Topic Name",
            "text": "Full question text",
            "difficulty": "easy|medium|hard",
            "type": "technical|behavioral|scenario",
            "ideal_points": ["key point 1", "key point 2", "key point 3"],
            "follow_up_prompts": ["if they miss X, ask this", "to go deeper, ask this"]
        }}
    ]
    
    Make questions specific to this role, not generic.
    Return ONLY the JSON array.
    """
    
    try:
        response = model.generate(prompt)
        text = response.text.strip()
        
        # Clean markdown formatting safely
        if "```" in text:
            parts = text.split("```")
            if len(parts) >= 2:
                text = parts[1]
                if text.startswith("json"):
                    text = text[4:]
        
        # Find JSON array in the text
        text = text.strip()
        if "[" in text:
            start = text.index("[")
            end = text.rfind("]") + 1
            if end > start:
                text = text[start:end]
        
        questions = json.loads(text)
        
        # Extract unique topics
        topics = {}
        for q in questions:
            topic = q.get("topic", "General")
            topics[topic] = topics.get(topic, 0) + 1
        
        topic_list = [
            {"name": name, "questions_allocated": count, "weight": count / len(questions)}
            for name, count in topics.items()
        ]
        
        return {
            "topics": topic_list,
            "questions": questions,
            "focus_areas": match.get("interview_focus_areas", []),
            "total_questions": len(questions)
        }
        
    except Exception as e:
        # Return fallback questions on error
        return {
            "topics": [{"name": "General", "questions_allocated": 3, "weight": 1.0}],
            "questions": [
                {
                    "topic": "Introduction",
                    "text": "Tell me about yourself and your interest in this role.",
                    "difficulty": "easy",
                    "type": "behavioral",
                    "ideal_points": ["Clear summary", "Relevant experience", "Motivation"],
                    "follow_up_prompts": []
                },
                {
                    "topic": "Experience",
                    "text": "Walk me through a challenging project you've worked on.",
                    "difficulty": "medium",
                    "type": "behavioral",
                    "ideal_points": ["Context", "Your actions", "Results"],
                    "follow_up_prompts": []
                },
                {
                    "topic": "Technical",
                    "text": f"What's your experience with {(jd.get('required_skills') or ['the required technologies'])[0] if jd.get('required_skills') else 'the required technologies'}?",
                    "difficulty": "medium",
                    "type": "technical",
                    "ideal_points": ["Hands-on experience", "Specific examples", "Depth of knowledge"],
                    "follow_up_prompts": []
                }
            ],
            "focus_areas": [],
            "total_questions": 3,
            "error": str(e)
        }


def generate_follow_up(question: dict, user_response: str, current_depth: int = 0) -> Optional[dict]:
    """
    Generate adaptive follow-up question based on user's response.
    
    Args:
        question: Original question dict
        user_response: User's answer text
        current_depth: How deep we've gone (0-3)
    
    Returns:
        Follow-up question dict or None if sufficient depth reached
    """
    if current_depth >= 3:
        return None
    
    from .tools import get_eval_model
    
    model = get_eval_model()
    
    prompt = f"""
    The candidate was asked: "{question['text']}"
    
    They answered: "{user_response[:1500]}"
    
    Ideal points to cover: {', '.join(question.get('ideal_points', []))}
    
    Current depth level: {current_depth} (0=surface, 3=very deep)
    
    Decide if we should:
    1. Ask a follow-up to go DEEPER on something they mentioned
    2. Ask about something they MISSED from ideal points
    3. Move on (return null)
    
    If follow-up needed, return JSON:
    {{
        "should_follow_up": true,
        "reason": "why we're asking this",
        "follow_up_text": "The full follow-up question",
        "target_point": "what ideal point this addresses"
    }}
    
    If their answer was good enough, return:
    {{
        "should_follow_up": false,
        "feedback": "Brief positive note about their answer"
    }}
    
    Return ONLY JSON.
    """
    
    try:
        response = model.generate(prompt)
        text = response.text.strip()
        
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()
        
        result = json.loads(text)
        
        if result.get("should_follow_up"):
            return {
                "topic": question.get("topic"),
                "text": result["follow_up_text"],
                "difficulty": question.get("difficulty"),
                "type": "follow_up",
                "parent_question": question["text"][:100],
                "depth": current_depth + 1,
                "ideal_points": [result.get("target_point", "Deeper understanding")]
            }
        return None
        
    except:
        return None


def get_next_question(interview_plan: dict, answered_indices: List[int], current_topic: str = None) -> Optional[dict]:
    """
    Get the next question, balancing topics and progression.
    
    Args:
        interview_plan: The generated interview plan
        answered_indices: List of already-answered question indices
        current_topic: Topic of the last question (for interleaving)
    
    Returns:
        Next question dict or None if all done
    """
    questions = interview_plan.get("questions", [])
    remaining = [(i, q) for i, q in enumerate(questions) if i not in answered_indices]
    
    if not remaining:
        return None
    
    # Try to switch topics for interleaving effect
    different_topic = [
        (i, q) for i, q in remaining 
        if q.get("topic") != current_topic
    ]
    
    if different_topic:
        remaining = different_topic
    
    # Pick randomly from remaining
    idx, question = random.choice(remaining)
    question["_index"] = idx
    
    return question
