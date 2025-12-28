"""
Interviewer Persona
Creates a conversational, human-like interview experience with an Indian persona
"""

import random
from typing import Optional

# Interviewer persona - Indian female
INTERVIEWER = {
    "name": "Ananya Iyer",
    "title": "Senior Technical Interviewer",
    "company": "MockMentor",
    "style": "warm, professional, encouraging",
    "avatar": "👩🏽‍💼",
    "voice": "en-IN-NeerjaNeural"  # Indian English female
}

# Conversation templates - natural, conversational
GREETINGS = [
    f"Hello! I'm {INTERVIEWER['name']}, and I'll be your interviewer today. It's nice to meet you. Take a moment to relax, and let's have a good conversation.",
    f"Hi there! My name is {INTERVIEWER['name']}. I'm really looking forward to learning more about you. This is meant to be a discussion, not an interrogation, so just be yourself.",
    f"Welcome! I'm {INTERVIEWER['name']}. I've gone through your profile and I'm quite interested to hear more. Ready when you are!"
]

# Short, conversational transitions
TRANSITIONS = {
    "first": [
        "Alright, let's begin.",
        "So, to start off...",
        "Let me ask you something first.",
    ],
    "next": [
        "Okay, moving on.",
        "That's good. Now,",
        "Interesting. Tell me,",
        "I see. Let me ask you this.",
        "Alright.",
    ],
    "follow_up": [
        "Can you tell me more about that?",
        "Interesting. Go deeper on that.",
        "Could you elaborate?",
    ],
    "technical": [
        "Now, a technical one.",
        "Let's get into the details.",
        "Here's a technical question.",
    ],
    "behavioral": [
        "Tell me about a time when...",
        "Share an experience where...",
        "Think of a situation when...",
    ],
    "closing": [
        "Almost there.",
        "One last thing.",
        "Final question.",
    ]
}

# Short acknowledgments for natural flow
ACKNOWLEDGMENTS = [
    "Okay.",
    "I see.",
    "Hmm.",
    "Right.",
    "Got it.",
    "Makes sense.",
    "Understood.",
]

ENCOURAGEMENTS = [
    "Take your time.",
    "No rush.",
    "Think about it.",
]

# Filler phrases for natural speech
FILLERS = [
    "So,",
    "Well,",
    "Now,",
    "Alright,",
]


def get_greeting() -> str:
    """Get a random greeting from the interviewer."""
    return random.choice(GREETINGS)


def get_transition(question_type: str = "next", question_num: int = 0, total: int = 15) -> str:
    """Get appropriate transition based on context."""
    if question_num == 0:
        return random.choice(TRANSITIONS["first"])
    elif question_num >= total - 2:
        return random.choice(TRANSITIONS["closing"])
    elif question_type == "technical":
        # Sometimes use technical transition, sometimes just next
        return random.choice(TRANSITIONS["technical"] + TRANSITIONS["next"])
    elif question_type == "behavioral":
        return random.choice(TRANSITIONS["behavioral"])
    else:
        return random.choice(TRANSITIONS["next"])


def get_acknowledgment() -> str:
    """Get a random short acknowledgment."""
    return random.choice(ACKNOWLEDGMENTS)


def get_filler() -> str:
    """Get a random filler for natural speech."""
    return random.choice(FILLERS)


def format_question_conversationally(
    question: dict, 
    question_num: int = 0, 
    total: int = 15,
    previous_answer: str = None
) -> str:
    """
    Format a question in a short, conversational way.
    Keeps responses brief for natural speech.
    """
    transition = get_transition(question.get("type", "next"), question_num, total)
    question_text = question.get("text", "")
    
    # Keep it short - just transition + question
    if previous_answer and question_num > 0:
        ack = get_acknowledgment()
        return f"{ack} {transition} {question_text}"
    else:
        return f"{transition} {question_text}"


def format_feedback_conversationally(score: float, feedback: str, is_last: bool = False) -> str:
    """Format evaluation feedback - keep it short and encouraging."""
    # Short opener based on score
    if score >= 8:
        opener = random.choice(["Great answer.", "Well done.", "Excellent."])
    elif score >= 6:
        opener = random.choice(["Good.", "Nice.", "That's good."])
    elif score >= 4:
        opener = random.choice(["Okay.", "Alright.", "Fair enough."])
    else:
        opener = random.choice(["I see.", "Okay."])
    
    # Keep feedback short - just one key point
    short_feedback = feedback.split('.')[0] + '.' if '.' in feedback else feedback
    
    if is_last:
        return f"{opener} {short_feedback} That's all for today. Thank you!"
    else:
        return f"{opener} {short_feedback}"


def get_interviewer_info() -> dict:
    """Return interviewer info for display."""
    return INTERVIEWER.copy()


def get_voice_id() -> str:
    """Get the TTS voice ID for the interviewer."""
    return INTERVIEWER["voice"]
