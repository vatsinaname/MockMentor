import streamlit as st
import sys
import os

# Load environment variables from .env file (local dev)
from dotenv import load_dotenv
load_dotenv()

# Load Streamlit Cloud secrets into environment (for cloud deployment)
try:
    if hasattr(st, 'secrets'):
        for key in ['MODEL_PROVIDER', 'MODEL_NAME', 'GROQ_API_KEY', 'GOOGLE_API_KEY']:
            if key in st.secrets:
                os.environ[key] = st.secrets[key]
except Exception:
    # No secrets.toml found - this is fine for local dev (uses .env instead)
    pass

# Apply nest_asyncio to allow nested event loops
import nest_asyncio
nest_asyncio.apply()

import asyncio

# Add parent directory to path so we can import mockmentor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mockmentor.agent import mock_mentor_agent
from mockmentor.tools import get_profile

# --- Page Config ---
st.set_page_config(
    page_title="MockMentor",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Minimal Professional CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .stApp {
        background: #09090b;
    }
    
    #MainMenu, footer {visibility: hidden;}
    
    section[data-testid="stSidebar"] {
        background: #09090b;
        border-right: 1px solid #27272a;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #fafafa !important;
        font-weight: 500 !important;
        background: none !important;
        -webkit-text-fill-color: #fafafa !important;
    }
    
    p, span, div {
        color: #a1a1aa;
    }
    
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    [data-testid="stChatMessage"] {
        padding: 16px 0;
        border-bottom: 1px solid #18181b;
    }
    
    .stChatInput > div {
        background: #18181b !important;
        border: 1px solid #27272a !important;
        border-radius: 6px;
    }
    
    .stChatInput textarea {
        color: #fafafa !important;
    }
    
    .stChatInput textarea::placeholder {
        color: #52525b !important;
    }
    
    div[data-testid="metric-container"] {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 6px;
        padding: 16px;
    }
    
    div[data-testid="metric-container"] label {
        color: #71717a !important;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #fafafa !important;
        font-weight: 500;
    }
    
    .stProgress > div > div {
        background: #3b82f6 !important;
    }
    
    .stButton > button {
        background: #18181b;
        color: #a1a1aa;
        border: 1px solid #27272a;
        border-radius: 6px;
        font-weight: 500;
        font-size: 13px;
    }
    
    .stButton > button:hover {
        background: #27272a;
        border-color: #3f3f46;
        color: #fafafa;
    }
    
    .stAlert {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 6px;
        color: #a1a1aa;
    }
    
    code {
        background: #18181b;
        padding: 2px 6px;
        border-radius: 4px;
        color: #60a5fa;
        font-size: 13px;
    }
    
    .stat-card {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .stat-label {
        color: #71717a;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    .stat-value {
        color: #fafafa;
        font-size: 24px;
        font-weight: 500;
    }
    
    .topic-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 12px;
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 6px;
        margin-bottom: 8px;
    }
    
    .topic-name {
        color: #fafafa;
        font-size: 13px;
        font-weight: 500;
    }
    
    .topic-score {
        color: #71717a;
        font-size: 12px;
    }
    
    .topic-score.low { color: #ef4444; }
    .topic-score.mid { color: #f59e0b; }
    .topic-score.high { color: #22c55e; }
    
    .section-header {
        color: #52525b;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 20px 0 12px 0;
        font-weight: 600;
    }
    
    .brand {
        color: #fafafa;
        font-size: 18px;
        font-weight: 600;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    
    .tagline {
        color: #52525b;
        font-size: 13px;
    }
    
    hr {
        border: none;
        border-top: 1px solid #27272a;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<p class="brand">MockMentor</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Data Engineering Interview Practice</p>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- Sidebar ---
profile = get_profile()
weak_areas = profile.get("weak_areas", {})
history = profile.get("history", [])

with st.sidebar:
    st.markdown('<p class="brand">MockMentor</p>', unsafe_allow_html=True)
    
    # Tabbed navigation
    tab1, tab2 = st.tabs(["Practice", "Analytics"])
    
    # ===== PRACTICE TAB =====
    with tab1:
        st.markdown('<p class="section-header">Quick Start</p>', unsafe_allow_html=True)
        
        # Quick action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Continue", use_container_width=True, help="Resume with optimal question"):
                st.session_state.practice_mode = "balanced"
                st.session_state.start_practice = True
        with col2:
            if st.button("Review", use_container_width=True, help="Questions due for review"):
                st.session_state.practice_mode = "review"
                st.session_state.start_practice = True
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Focus", use_container_width=True, help="Target weak areas"):
                st.session_state.practice_mode = "focus"
                st.session_state.start_practice = True
        with col4:
            if st.button("Explore", use_container_width=True, help="Try new questions"):
                st.session_state.practice_mode = "explore"
                st.session_state.start_practice = True
        
        st.markdown('<p class="section-header">Topics</p>', unsafe_allow_html=True)
        
        # Topic buttons in a compact grid
        topics = [
            ("SQL", "sql"), ("Pipelines", "pipelines"), 
            ("Modeling", "modeling"), ("System Design", "system_design"),
            ("Debugging", "debugging"), ("Cloud", "cloud"),
            ("Python", "python"), ("Data Quality", "data_quality")
        ]
        
        for i in range(0, len(topics), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(topics):
                    name, topic_id = topics[i + j]
                    with col:
                        if st.button(name, key=f"topic_{topic_id}", use_container_width=True):
                            st.session_state.selected_topic = topic_id
                            st.session_state.start_practice = True
        
        st.markdown('<p class="section-header">Session</p>', unsafe_allow_html=True)
        
        if st.button("Reset Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Session cleared. Select a topic or practice mode to begin."
            })
            st.rerun()
    
    # ===== ANALYTICS TAB =====
    with tab2:
        try:
            from mockmentor.tools import get_analytics
            analytics = get_analytics()
            
            st.markdown('<p class="section-header">Overview</p>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Answered", analytics["total_questions_answered"])
            with col2:
                due = analytics["due_for_review"]
                st.metric("Due for Review", due)
            
            st.markdown('<p class="section-header">Topic Mastery</p>', unsafe_allow_html=True)
            
            topic_mastery = analytics.get("topic_mastery", {})
            if topic_mastery:
                # Sort by mastery percentage
                sorted_topics = sorted(
                    topic_mastery.items(), 
                    key=lambda x: x[1].get("mastery_percentage", 0)
                )
                for topic, stats in sorted_topics:
                    mastery_pct = stats.get("mastery_percentage", 0)
                    mastered = stats.get("mastered_count", 0)
                    total = stats.get("total_questions", 0)
                    
                    score_class = "low" if mastery_pct < 40 else "mid" if mastery_pct < 70 else "high"
                    st.markdown(f'''
                        <div class="topic-row">
                            <span class="topic-name">{topic.replace("_", " ").title()}</span>
                            <span class="topic-score {score_class}">{mastered}/{total}</span>
                        </div>
                    ''', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color: #52525b; font-size: 13px;">No practice data yet</p>', unsafe_allow_html=True)
            
            # Recommendations
            recs = analytics.get("recommendations", {})
            if recs.get("recommended_mode"):
                st.markdown('<p class="section-header">Recommendation</p>', unsafe_allow_html=True)
                mode = recs["recommended_mode"]
                if mode == "review":
                    st.info(f"You have {recs['due_count']} questions due for review")
                elif mode == "focus":
                    topic = recs.get("suggested_topic", "").replace("_", " ").title()
                    st.info(f"Focus on: {topic}")
                else:
                    st.info("Explore new topics to expand coverage")
                    
        except Exception as e:
            st.markdown('<p style="color: #52525b; font-size: 13px;">Analytics loading...</p>', unsafe_allow_html=True)

# --- Async Helper ---
async def run_agent_with_session(runner, user_id, session_id, message_content):
    from google.genai.types import Content, Part
    
    app_name = runner.app_name
    
    session = None
    try:
        session = await runner.session_service.get_session(
            app_name=app_name,
            user_id=user_id, 
            session_id=session_id
        )
    except Exception:
        pass
    
    if session is None:
        session = await runner.session_service.create_session(
            app_name=app_name,
            user_id=user_id, 
            session_id=session_id
        )
    
    msg_obj = Content(role="user", parts=[Part(text=message_content)])
    
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=msg_obj
    ):
        if hasattr(event, 'is_final_response') and event.is_final_response():
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text
        elif hasattr(event, 'text') and event.text:
            response_text = event.text
    
    return response_text

# --- Chat Logic ---

# Initialize messages if not present
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Welcome. I will help you prepare for Data Engineering interviews with realistic questions and detailed feedback.\n\nUse the **Practice** tab to:\n- **Continue** — Resume with an optimally-selected question\n- **Review** — Practice questions due for spaced repetition\n- **Focus** — Target your weakest areas\n- **Explore** — Try new questions\n\nOr select a specific topic to dive deep."
    })

# Handle practice mode button clicks - set pending prompt
if st.session_state.get("start_practice"):
    from mockmentor.tools import select_smart_question
    
    mode = st.session_state.get("practice_mode", "balanced")
    topic = st.session_state.get("selected_topic")
    
    # Select question using learning engine
    question = select_smart_question(mode=mode, topic=topic)
    
    if "error" in question:
        pending = f"I want to practice {topic if topic else 'any topic'}"
    else:
        # Format the question for the agent
        topic_name = question.get("topic", "").replace("_", " ").title()
        difficulty = question.get("difficulty", "medium").title()
        pending = f"Give me a {difficulty.lower()} {topic_name} question"
    
    # Set pending prompt and clear flags
    st.session_state.pending_prompt = pending
    st.session_state.start_practice = False
    st.session_state.practice_mode = None
    st.session_state.selected_topic = None

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get prompt: either from chat input OR from pending button action
# IMPORTANT: st.chat_input must always be rendered for the input box to appear
user_input = st.chat_input("Enter your response")

# Check for pending prompt from button click
pending = st.session_state.get("pending_prompt")
if pending:
    st.session_state.pending_prompt = None

# Use pending prompt if available, otherwise use user input
prompt = pending or user_input

# Process the prompt if we have one
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            try:
                if "runner" not in st.session_state:
                    from google.adk.runners import InMemoryRunner
                    st.session_state.runner = InMemoryRunner(
                        agent=mock_mentor_agent,
                        app_name="MockMentor"
                    )
                
                runner = st.session_state.runner
                
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                response_text = loop.run_until_complete(
                    run_agent_with_session(runner, "user", "default", prompt)
                )
                
                if response_text:
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    st.warning("No response received.")
                    
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "EXHAUSTED" in error_msg:
                    st.error("Rate limit exceeded. Please wait and retry.")
                else:
                    st.error(f"Error: {e}")

