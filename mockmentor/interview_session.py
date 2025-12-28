"""
Interview Session Manager
Manages the interview flow, state, and evaluation
"""

import json
from datetime import datetime
from typing import Optional, List, Dict
import streamlit as st


class InterviewSession:
    """Manages an interview session state."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset session to initial state."""
        self.resume = None
        self.jd = None
        self.match_result = None
        self.interview_plan = None
        self.current_question_idx = 0
        self.current_depth = 0
        self.answers = []
        self.voice_metrics = []
        self.started_at = None
        self.mode = "text"  # "text" or "voice"
    
    def start_interview(self, resume: dict, jd: dict, match: dict, plan: dict):
        """Initialize interview with parsed data."""
        self.resume = resume
        self.jd = jd
        self.match_result = match
        self.interview_plan = plan
        self.started_at = datetime.now().isoformat()
        self.answers = []
        self.current_question_idx = 0
        self.current_depth = 0
    
    def get_current_question(self) -> Optional[dict]:
        """Get the current question to ask."""
        if not self.interview_plan:
            return None
        
        questions = self.interview_plan.get("questions", [])
        if self.current_question_idx >= len(questions):
            return None
        
        return questions[self.current_question_idx]
    
    def record_answer(self, answer_text: str, score: float, feedback: str, 
                      voice_metrics: dict = None):
        """Record an answer and its evaluation."""
        question = self.get_current_question()
        
        self.answers.append({
            "question_idx": self.current_question_idx,
            "question": question.get("text") if question else "",
            "topic": question.get("topic") if question else "",
            "answer": answer_text,
            "score": score,
            "feedback": feedback,
            "depth": self.current_depth,
            "timestamp": datetime.now().isoformat()
        })
        
        if voice_metrics:
            self.voice_metrics.append({
                "question_idx": self.current_question_idx,
                **voice_metrics
            })
    
    def advance_question(self):
        """Move to next question."""
        self.current_question_idx += 1
        self.current_depth = 0
    
    def increase_depth(self):
        """Track depth increase for follow-up."""
        self.current_depth += 1
    
    def is_complete(self) -> bool:
        """Check if interview is complete."""
        if not self.interview_plan:
            return True
        return self.current_question_idx >= len(self.interview_plan.get("questions", []))
    
    def get_progress(self) -> dict:
        """Get current progress stats."""
        total = len(self.interview_plan.get("questions", [])) if self.interview_plan else 0
        answered = len(self.answers)
        
        return {
            "current": self.current_question_idx + 1,
            "total": total,
            "answered": answered,
            "percentage": (self.current_question_idx / total * 100) if total > 0 else 0
        }
    
    def generate_final_report(self) -> dict:
        """Generate comprehensive final evaluation report."""
        if not self.answers:
            return {"error": "No answers recorded"}
        
        # Calculate aggregate scores
        scores = [a["score"] for a in self.answers if a.get("score")]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Group by topic
        topic_scores = {}
        for answer in self.answers:
            topic = answer.get("topic", "General")
            if topic not in topic_scores:
                topic_scores[topic] = []
            topic_scores[topic].append(answer.get("score", 0))
        
        topic_averages = {
            topic: sum(s) / len(s) 
            for topic, s in topic_scores.items()
        }
        
        # Voice analysis aggregate
        voice_summary = None
        if self.voice_metrics:
            total_fillers = sum(m.get("filler_words", {}).get("count", 0) for m in self.voice_metrics)
            total_words = sum(m.get("word_count", 0) for m in self.voice_metrics)
            filler_ratio = total_fillers / total_words if total_words > 0 else 0
            
            voice_summary = {
                "total_words_spoken": total_words,
                "total_filler_words": total_fillers,
                "filler_ratio": round(filler_ratio * 100, 1),
                "fluency_rating": "excellent" if filler_ratio < 0.02 else 
                                 "good" if filler_ratio < 0.05 else "needs improvement"
            }
        
        # Identify strengths and areas for improvement
        strong_topics = [t for t, s in topic_averages.items() if s >= 7]
        weak_topics = [t for t, s in topic_averages.items() if s < 6]
        
        return {
            "overall_score": round(avg_score * 10, 1),  # Convert to 0-100
            "questions_answered": len(self.answers),
            "topic_breakdown": topic_averages,
            "strong_areas": strong_topics,
            "improvement_areas": weak_topics,
            "voice_analysis": voice_summary,
            "match_score": self.match_result.get("overall_score") if self.match_result else None,
            "job_title": self.jd.get("title") if self.jd else None,
            "duration_minutes": self._calculate_duration(),
            "detailed_answers": self.answers
        }
    
    def _calculate_duration(self) -> float:
        """Calculate session duration in minutes."""
        if not self.started_at:
            return 0
        try:
            start = datetime.fromisoformat(self.started_at)
            duration = datetime.now() - start
            return round(duration.total_seconds() / 60, 1)
        except:
            return 0


def get_session() -> InterviewSession:
    """Get or create session from Streamlit state."""
    if "interview_session" not in st.session_state:
        st.session_state.interview_session = InterviewSession()
    return st.session_state.interview_session


def reset_session():
    """Reset the interview session."""
    st.session_state.interview_session = InterviewSession()
