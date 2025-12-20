import random
import json
import os
from datetime import datetime


def get_eval_model():
    """Returns the appropriate model for evaluation based on environment config."""
    provider = os.environ.get("MODEL_PROVIDER", "groq").lower()
    
    if provider == "gemini":
        from google.adk.models import Gemini
        model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")
        return Gemini(model=model_name)
    else:
        from google.adk.models import LiteLlm
        model_name = os.environ.get("MODEL_NAME", "moonshotai/kimi-k2-instruct")
        if not model_name.startswith("groq/"):
            model_name = f"groq/{model_name}"
        return LiteLlm(model=model_name)
from .questions import QUESTIONS
from .rubrics import RUBRICS

DB_FILE = "mockmentor_db.json"

def _load_db():
    if not os.path.exists(DB_FILE):
        return {
            "default_user": {
                "weak_areas": {},
                "history": [],
                "questions_seen": [],
                "question_mastery": {},  # Per-question spaced repetition data
                "session_stats": {
                    "total_time_seconds": 0,
                    "sessions_count": 0
                }
            }
        }
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            # Ensure new fields exist for backward compatibility
            user = data.get("default_user", {})
            if "question_mastery" not in user:
                user["question_mastery"] = {}
            if "session_stats" not in user:
                user["session_stats"] = {"total_time_seconds": 0, "sessions_count": 0}
            data["default_user"] = user
            return data
    except:
         return {"default_user": {"weak_areas": {}, "history": [], "questions_seen": [], "question_mastery": {}, "session_stats": {"total_time_seconds": 0, "sessions_count": 0}}}

def _save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def _get_user_data():
    db = _load_db()
    return db["default_user"]

def _save_user_data(user_data):
    db = _load_db()
    db["default_user"] = user_data
    _save_db(db)

def select_question(topic: str = None, difficulty: str = None) -> dict:
    """
    Selects an appropriate interview question based on user's weak areas and history.
    Topic options: sql, pipelines, modeling, system_design, debugging
    """
    user = _get_user_data()
    seen = set(user["questions_seen"])
    
    # Normalize topic name for matching
    topic_map = {
        "sql": "sql",
        "pipelines": "pipelines",
        "pipeline": "pipelines",
        "data pipelines": "pipelines",
        "modeling": "modeling",
        "data modeling": "modeling",
        "model": "modeling",
        "system design": "system_design",
        "system_design": "system_design",
        "sys design": "system_design",
        "sysdesign": "system_design",
        "debugging": "debugging",
        "debug": "debugging",
        "cloud": "cloud",
        "cloud infrastructure": "cloud",
        "infrastructure": "cloud",
        "aws": "cloud",
        "gcp": "cloud",
        "azure": "cloud",
        "python": "python",
        "coding": "python",
        "python coding": "python",
        "data quality": "data_quality",
        "data_quality": "data_quality",
        "quality": "data_quality",
        "dq": "data_quality",
    }
    
    if topic:
        topic_lower = topic.lower().strip()
        topic = topic_map.get(topic_lower, topic_lower)
    
    candidates = []
    for q_id, q in QUESTIONS.items():
        if q_id in seen:
            continue
        if topic and q["topic"] != topic:
            continue
        if difficulty and q.get("difficulty") != difficulty.lower():
            continue
        candidates.append(q)
    
    if not candidates:
        if topic:
             return {"error": f"No more questions available for topic: {topic}. Available topics: sql, pipelines, modeling, system_design, debugging, cloud, python, data_quality"}
        # If no new questions, maybe revisit old ones? For now, just reset pool or fallback
        candidates = list(QUESTIONS.values()) 

    scored_candidates = []
    for q in candidates:
        t = q["topic"]
        score = user["weak_areas"].get(t, 0.5)
        weight = 1.0 - score + 0.1
        scored_candidates.append((q, weight))
    
    total_weight = sum(w for q, w in scored_candidates)
    r = random.uniform(0, total_weight)
    upto = 0
    selected_q = candidates[0]
    for q, w in scored_candidates:
        if upto + w >= r:
            selected_q = q
            break
        upto += w
        
    return selected_q

def evaluate_response(question_id: str, user_response: str) -> dict:
    """
    Evaluates the user's response against the ideal answer and rubric.
    """
    if question_id not in QUESTIONS:
        return {"error": "Invalid Question ID"}
        
    question = QUESTIONS[question_id]
    rubric = RUBRICS["default"]
    
    eval_model = get_eval_model()
    
    prompt = f"""
    You are an expert interviewer. Grade this answer.
    
    Question: {question['text']}
    Ideal Answer Points: {', '.join(question['ideal_points'])}
    
    User Answer: {user_response}
    
    Rubric:
    - Accuracy (Weight {rubric['accuracy']['weight']}): {rubric['accuracy']['description']}
    - Completeness (Weight {rubric['completeness']['weight']}): {rubric['completeness']['description']}
    - Clarity (Weight {rubric['clarity']['weight']}): {rubric['clarity']['description']}
    
    Return JSON only:
    {{
        "accuracy_score": (0-10),
        "completeness_score": (0-10),
        "clarity_score": (0-10),
        "overall_score": (0-10),
        "feedback": "string",
        "key_gap": "string"
    }}
    """
    
    try:
        response = eval_model.generate(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
    except Exception as e:
        result = {
            "accuracy_score": 5,
            "overall_score": 5,
            "feedback": f"Grading error: {str(e)}. Good effort though.",
            "key_gap": "Unknown"
        }

    # Atomic-ish update
    user = _get_user_data()
    topic = question["topic"]
    
    current_topic_score = user["weak_areas"].get(topic, 0.5)
    new_score = (current_topic_score * 0.7) + ((result["overall_score"] / 10.0) * 0.3)
    user["weak_areas"][topic] = new_score
    
    user["history"].append({
        "question_id": question_id,
        "score": result["overall_score"],
        "topic": topic,
        "date": datetime.now().isoformat()[:10]
    })
    if question_id not in user["questions_seen"]:
        user["questions_seen"].append(question_id)
        
    _save_user_data(user)
    
    return result

def get_profile() -> dict:
    return _get_user_data()

def create_usage_report() -> str:
    user = _get_user_data()
    hist = user["history"]
    if not hist:
        return "No sessions recorded yet."
        
    avg_score = sum(h["score"] for h in hist) / len(hist)
    
    if user["weak_areas"]:
        weakest_link = min(user["weak_areas"].items(), key=lambda x: x[1])
        weakest_str = f"{weakest_link[0]} ({weakest_link[1]:.2f})"
    else:
        weakest_str = "None identified"
    
    return f"""
    Sessions: {len(hist)}
    Average Score: {avg_score:.1f}/10
    Weakest Area: {weakest_str}
    Questions Answered: {len(hist)}
    """


# --- Learning Engine Integration ---

def update_mastery(question_id: str, score: float, confidence: int = 2) -> dict:
    """
    Update mastery data for a question after practice.
    
    Args:
        question_id: The question ID
        score: Score 0-10 from evaluation
        confidence: Self-assessed confidence 1-3 (1=need practice, 2=partial, 3=confident)
    
    Returns:
        Updated question mastery data
    """
    from .learning_engine import update_question_mastery
    
    user = _get_user_data()
    question_mastery = user.get("question_mastery", {})
    
    updated_data = update_question_mastery(question_id, score, confidence, question_mastery)
    question_mastery[question_id] = updated_data
    
    user["question_mastery"] = question_mastery
    _save_user_data(user)
    
    return updated_data


def get_analytics() -> dict:
    """
    Get comprehensive analytics for the Stats tab.
    
    Returns:
        {
            "total_questions_answered": int,
            "total_sessions": int,
            "topic_mastery": {topic: {stats}},
            "weak_topics": [(topic, percentage)],
            "due_for_review": int,
            "recent_scores": [last 10 scores],
            "recommendations": {...}
        }
    """
    from .learning_engine import (
        calculate_topic_mastery, 
        get_weak_topics, 
        get_practice_recommendations
    )
    
    user = _get_user_data()
    history = user.get("history", [])
    question_mastery = user.get("question_mastery", {})
    
    questions_list = list(QUESTIONS.values())
    
    # Calculate per-topic mastery
    topics = set(q["topic"] for q in questions_list)
    topic_mastery = {}
    for topic in topics:
        topic_mastery[topic] = calculate_topic_mastery(topic, questions_list, question_mastery)
    
    # Get weak topics and recommendations
    weak_topics = get_weak_topics(questions_list, question_mastery)
    recommendations = get_practice_recommendations(questions_list, question_mastery)
    
    # Recent scores
    recent_scores = [h["score"] for h in history[-10:]]
    
    return {
        "total_questions_answered": len(history),
        "total_sessions": len(set(h.get("date", "") for h in history)),
        "topic_mastery": topic_mastery,
        "weak_topics": weak_topics,
        "due_for_review": recommendations["due_count"],
        "recent_scores": recent_scores,
        "recommendations": recommendations
    }


def select_smart_question(mode: str = "balanced", topic: str = None) -> dict:
    """
    Select a question using learning engine algorithms.
    
    Modes:
        - "review": Prioritize questions due for spaced repetition review
        - "focus": Target weakest topic
        - "balanced": Interleaved practice across topics
        - "explore": Prioritize unseen questions
    
    Args:
        mode: Selection strategy
        topic: Optional topic filter
    
    Returns:
        Selected question dict
    """
    from .learning_engine import (
        select_interleaved_questions,
        is_due_for_review,
        get_weak_topics
    )
    
    user = _get_user_data()
    question_mastery = user.get("question_mastery", {})
    questions_list = list(QUESTIONS.values())
    
    # Filter by topic if specified
    if topic:
        topic_map = {
            "sql": "sql", "pipelines": "pipelines", "modeling": "modeling",
            "system_design": "system_design", "debugging": "debugging",
            "cloud": "cloud", "python": "python", "data_quality": "data_quality"
        }
        normalized_topic = topic_map.get(topic.lower().strip(), topic.lower())
        questions_list = [q for q in questions_list if q["topic"] == normalized_topic]
    
    if not questions_list:
        return {"error": "No questions available for the specified criteria"}
    
    if mode == "review":
        # Prioritize due questions
        due_questions = [
            q for q in questions_list 
            if is_due_for_review(question_mastery.get(q["id"], {}))
        ]
        if due_questions:
            questions_list = due_questions
    
    elif mode == "focus":
        # Target weakest topic
        weak = get_weak_topics(questions_list, question_mastery, top_n=1)
        if weak:
            weakest_topic = weak[0][0]
            questions_list = [q for q in questions_list if q["topic"] == weakest_topic]
    
    elif mode == "explore":
        # Prioritize unseen
        unseen = [
            q for q in questions_list 
            if question_mastery.get(q["id"], {}).get("attempts", 0) == 0
        ]
        if unseen:
            questions_list = unseen
    
    # Use interleaving for final selection
    selected = select_interleaved_questions(
        questions_list, 
        question_mastery, 
        count=1
    )
    
    return selected[0] if selected else {"error": "No questions available"}


def get_topic_list() -> list:
    """
    Get list of all available topics with question counts.
    
    Returns:
        [{"id": str, "name": str, "count": int}, ...]
    """
    from .questions import TOPICS
    
    result = []
    for topic_id, topic_info in TOPICS.items():
        count = len([q for q in QUESTIONS.values() if q["topic"] == topic_id])
        result.append({
            "id": topic_id,
            "name": topic_info["name"],
            "description": topic_info.get("description", ""),
            "count": count
        })
    
    return result
