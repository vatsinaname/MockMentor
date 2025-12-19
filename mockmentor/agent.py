
from google.adk.agents import Agent
from google.adk.model import Model
from .tools import select_question, evaluate_response, get_profile, create_usage_report
from .prompts import MOCKMENTOR_INSTRUCTION

# Initialize Model
model = Model(model_name="gemini-2.0-flash")

def _get_context_str():
    # Helper to inject dynamic context into the system prompt
    profile = get_profile()
    weak_areas = profile.get("weak_areas", {})
    sorted_weak = sorted(weak_areas.items(), key=lambda x: x[1])
    
    summary = ", ".join([f"{k}: {v:.1f}" for k, v in sorted_weak])
    return f"""
    Weak Areas: {summary if summary else "None yet"}
    Questions Attempted: {len(profile.get("history", []))}
    """

# Wrap instruction to be a callable or string. 
# ADK instructions can be static strings. Dynamic injection logic
# is usually handled by the agent loop or prompt formatting.
# For this version, we will prepend context in the tool output or assume
# the agent reads state via tools.
# However, to make it "Feel" like it knows you, we can do a trick:
# The `instruction` arg matches the prompt.

final_instruction = MOCKMENTOR_INSTRUCTION.format(
    user_context_str="(Dynamic context will be loaded via tools)"
)

mock_mentor_agent = Agent(
    name="MockMentor",
    model=model,
    intro="Hello! I'm MockMentor. Ready to crush your Data Engineering interview? Let's start. What topic do you want to practice?",
    tools=[select_question, evaluate_response, get_profile, create_usage_report],
    instruction=final_instruction
)
