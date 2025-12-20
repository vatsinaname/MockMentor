"""
MockMentor Learning Engine
Evidence-based learning algorithms: spaced repetition, interleaving, mastery tracking
"""

import random
from datetime import datetime, timedelta
from typing import Optional


# Spaced repetition intervals (in days) based on mastery level
REVIEW_INTERVALS = {
    0: 0,      # New/Failed - immediate review
    1: 1,      # Learning - 1 day
    2: 3,      # Reviewing - 3 days
    3: 7,      # Confident - 1 week
    4: 14,     # Mastered - 2 weeks
    5: 30,     # Expert - 1 month
}


def calculate_mastery_level(question_data: dict) -> int:
    """
    Calculate mastery level (0-5) for a question based on:
    - Number of correct attempts
    - Self-assessed confidence
    - Time since last practice
    
    Returns:
        0 = New/Struggled
        1 = Learning
        2 = Reviewing
        3 = Confident
        4 = Mastered
        5 = Expert
    """
    attempts = question_data.get("attempts", 0)
    correct = question_data.get("correct_count", 0)
    confidence = question_data.get("avg_confidence", 0)  # 1-3 scale
    
    if attempts == 0:
        return 0
    
    success_rate = correct / attempts if attempts > 0 else 0
    
    # Combined score (0-1 range)
    score = (success_rate * 0.6) + ((confidence / 3) * 0.4)
    
    if score >= 0.9 and attempts >= 3:
        return 5  # Expert
    elif score >= 0.8 and attempts >= 2:
        return 4  # Mastered
    elif score >= 0.7:
        return 3  # Confident
    elif score >= 0.5:
        return 2  # Reviewing
    elif score >= 0.3:
        return 1  # Learning
    else:
        return 0  # Struggled


def get_next_review_date(mastery_level: int, last_reviewed: str = None) -> str:
    """
    Calculate when a question should next be reviewed based on mastery level.
    
    Args:
        mastery_level: 0-5 mastery level
        last_reviewed: ISO date string of last review
    
    Returns:
        ISO date string for next review
    """
    if last_reviewed:
        try:
            last_date = datetime.fromisoformat(last_reviewed)
        except:
            last_date = datetime.now()
    else:
        last_date = datetime.now()
    
    interval = REVIEW_INTERVALS.get(mastery_level, 0)
    next_date = last_date + timedelta(days=interval)
    
    return next_date.isoformat()[:10]  # Return date only


def is_due_for_review(question_data: dict) -> bool:
    """Check if a question is due for spaced repetition review."""
    next_review = question_data.get("next_review")
    
    if not next_review:
        return True  # Never reviewed = due now
    
    try:
        next_date = datetime.fromisoformat(next_review)
        return datetime.now() >= next_date
    except:
        return True


def select_interleaved_questions(
    questions: list,
    question_mastery: dict,
    count: int = 5,
    current_topic: str = None
) -> list:
    """
    Select questions using interleaved practice - mix topics for better retention.
    
    Prioritizes:
    1. Questions due for review (spaced repetition)
    2. Questions in weak areas
    3. Variety across topics
    """
    if not questions:
        return []
    
    # Categorize questions
    due_for_review = []
    not_yet_due = []
    unseen = []
    
    for q in questions:
        q_id = q["id"]
        q_data = question_mastery.get(q_id, {})
        
        if q_data.get("attempts", 0) == 0:
            unseen.append((q, 1.0))  # Unseen questions
        elif is_due_for_review(q_data):
            # Weight by inverse mastery (weaker = higher priority)
            mastery = calculate_mastery_level(q_data)
            weight = (5 - mastery) / 5 + 0.1
            due_for_review.append((q, weight))
        else:
            not_yet_due.append((q, 0.1))
    
    # Combine pools with priority: due > unseen > not_yet_due
    all_weighted = due_for_review + unseen + not_yet_due
    
    # Apply interleaving: ensure topic variety
    selected = []
    recent_topics = []
    
    while len(selected) < count and all_weighted:
        # Filter candidates to prefer different topics (interleaving)
        available = [
            (q, w) for q, w in all_weighted 
            if q["topic"] not in recent_topics[-2:] or len(all_weighted) <= 3
        ]
        
        if not available:
            available = all_weighted
        
        # Weighted random selection
        total_weight = sum(w for _, w in available)
        r = random.uniform(0, total_weight)
        cumulative = 0
        
        chosen = available[0][0]
        for q, w in available:
            cumulative += w
            if cumulative >= r:
                chosen = q
                break
        
        selected.append(chosen)
        recent_topics.append(chosen["topic"])
        all_weighted = [(q, w) for q, w in all_weighted if q["id"] != chosen["id"]]
    
    return selected


def calculate_topic_mastery(topic: str, questions: list, question_mastery: dict) -> dict:
    """
    Calculate overall mastery stats for a topic.
    
    Returns:
        {
            "total_questions": int,
            "mastered_count": int,  # mastery level >= 3
            "mastery_percentage": float,
            "avg_score": float,
            "due_for_review": int
        }
    """
    topic_questions = [q for q in questions if q.get("topic") == topic]
    
    if not topic_questions:
        return {
            "total_questions": 0,
            "mastered_count": 0,
            "mastery_percentage": 0.0,
            "avg_score": 0.0,
            "due_for_review": 0
        }
    
    mastered = 0
    total_score = 0
    attempted = 0
    due_count = 0
    
    for q in topic_questions:
        q_id = q["id"]
        q_data = question_mastery.get(q_id, {})
        
        if q_data.get("attempts", 0) > 0:
            attempted += 1
            mastery_level = calculate_mastery_level(q_data)
            
            if mastery_level >= 3:
                mastered += 1
            
            total_score += q_data.get("last_score", 0)
            
            if is_due_for_review(q_data):
                due_count += 1
        else:
            due_count += 1  # Unseen = due
    
    return {
        "total_questions": len(topic_questions),
        "mastered_count": mastered,
        "mastery_percentage": (mastered / len(topic_questions)) * 100 if topic_questions else 0,
        "avg_score": total_score / attempted if attempted > 0 else 0,
        "due_for_review": due_count
    }


def update_question_mastery(
    question_id: str,
    score: float,
    confidence: int,
    question_mastery: dict
) -> dict:
    """
    Update mastery data for a question after practice.
    
    Args:
        question_id: The question ID
        score: Score 0-10 from evaluation
        confidence: Self-assessed confidence 1-3 (1=need practice, 2=partial, 3=confident)
        question_mastery: Current mastery data dict
    
    Returns:
        Updated question mastery dict for this question
    """
    q_data = question_mastery.get(question_id, {
        "attempts": 0,
        "correct_count": 0,
        "avg_confidence": 0,
        "last_score": 0,
        "last_reviewed": None,
        "next_review": None,
        "scores": []
    })
    
    # Update attempt count
    q_data["attempts"] = q_data.get("attempts", 0) + 1
    
    # Track if "correct" (score >= 7)
    if score >= 7:
        q_data["correct_count"] = q_data.get("correct_count", 0) + 1
    
    # Update rolling average confidence
    old_conf = q_data.get("avg_confidence", confidence)
    attempts = q_data["attempts"]
    q_data["avg_confidence"] = ((old_conf * (attempts - 1)) + confidence) / attempts
    
    # Store score
    q_data["last_score"] = score
    scores = q_data.get("scores", [])
    scores.append(score)
    q_data["scores"] = scores[-10:]  # Keep last 10
    
    # Update review dates
    today = datetime.now().isoformat()[:10]
    q_data["last_reviewed"] = today
    
    mastery_level = calculate_mastery_level(q_data)
    q_data["next_review"] = get_next_review_date(mastery_level, today)
    q_data["mastery_level"] = mastery_level
    
    return q_data


def get_weak_topics(questions: list, question_mastery: dict, top_n: int = 3) -> list:
    """
    Identify the weakest topics for focused practice.
    
    Returns:
        List of (topic, mastery_percentage) tuples, sorted weakest first
    """
    topics = set(q["topic"] for q in questions)
    topic_scores = []
    
    for topic in topics:
        stats = calculate_topic_mastery(topic, questions, question_mastery)
        topic_scores.append((topic, stats["mastery_percentage"]))
    
    # Sort by mastery ascending (weakest first)
    topic_scores.sort(key=lambda x: x[1])
    
    return topic_scores[:top_n]


def get_practice_recommendations(questions: list, question_mastery: dict) -> dict:
    """
    Generate practice recommendations based on current state.
    
    Returns:
        {
            "due_count": int,
            "weak_topics": list,
            "recommended_mode": str,  # "review", "focus", "explore"
            "suggested_topic": str
        }
    """
    # Count questions due for review
    due_count = sum(
        1 for q in questions
        if is_due_for_review(question_mastery.get(q["id"], {}))
    )
    
    weak_topics = get_weak_topics(questions, question_mastery)
    
    # Determine recommended mode
    if due_count > 5:
        mode = "review"
        suggested_topic = None
    elif weak_topics and weak_topics[0][1] < 50:
        mode = "focus"
        suggested_topic = weak_topics[0][0]
    else:
        mode = "explore"
        suggested_topic = None
    
    return {
        "due_count": due_count,
        "weak_topics": weak_topics,
        "recommended_mode": mode,
        "suggested_topic": suggested_topic
    }
