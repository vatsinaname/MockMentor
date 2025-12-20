
import os
from google.adk.agents import Agent
from .tools import select_question, evaluate_response, get_profile, create_usage_report
from .prompts import MOCKMENTOR_INSTRUCTION


def get_model():
    """
    Returns the appropriate model based on environment configuration.
    
    Environment variables:
        MODEL_PROVIDER: "groq" or "gemini" (default: "groq")
        MODEL_NAME: Specific model name (defaults based on provider)
    """
    provider = os.environ.get("MODEL_PROVIDER", "groq").lower()
    
    if provider == "gemini":
        from google.adk.models import Gemini
        model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")
        return Gemini(model=model_name)
    else:
        # Default to Groq via LiteLLM
        from google.adk.models import LiteLlm
        model_name = os.environ.get("MODEL_NAME", "moonshotai/kimi-k2-instruct")
        # LiteLLM requires groq/ prefix for Groq models
        if not model_name.startswith("groq/"):
            model_name = f"groq/{model_name}"
        return LiteLlm(model=model_name)


# Initialize Model
model = get_model()

def _get_context_str():
    profile = get_profile()
    weak_areas = profile.get("weak_areas", {})
    sorted_weak = sorted(weak_areas.items(), key=lambda x: x[1])
    
    summary = ", ".join([f"{k}: {v:.1f}" for k, v in sorted_weak])
    return f"""
    Weak Areas: {summary if summary else "None yet"}
    Questions Attempted: {len(profile.get("history", []))}
    """

final_instruction = MOCKMENTOR_INSTRUCTION.format(
    user_context_str="(Dynamic context will be loaded via tools)"
)

mock_mentor_agent = Agent(
    name="MockMentor",
    model=model,
    tools=[select_question, evaluate_response, get_profile, create_usage_report],
    instruction=final_instruction
)
