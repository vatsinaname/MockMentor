import random
import json
import os
from google.adk.model import Model
from .questions import QUESTIONS
from .rubrics import RUBRICS

DB_FILE = "mockmentor_db.json"

def _load_db():
    if not os.path.exists(DB_FILE):
        return {
            "default_user": {
                "weak_areas": {},
                "history": [],
                "questions_seen": []
            }
        }
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
         return {"default_user": {"weak_areas": {}, "history": [], "questions_seen": []}}

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
    """
    user = _get_user_data()
    seen = set(user["questions_seen"])
    
    candidates = []
    for q_id, q in QUESTIONS.items():
        if q_id in seen:
            continue
        if topic and q["topic"] != topic:
            continue
        candidates.append(q)
    
    if not candidates:
        if topic:
             return {"error": f"No more questions available for topic: {topic}"}
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
    
    eval_model = Model(model_name="gemini-2.0-flash")
    
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
        "date": "2024-12-19" # simplified
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
