import streamlit as st
import sys
import os

# Add parent directory to path so we can import mockmentor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mockmentor.agent import mock_mentor_agent
from mockmentor.tools import get_profile

# --- Page Config ---
st.set_page_config(
    page_title="MockMentor AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for "Futuristic/Google" Feel ---
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Neon Glows & Gradients */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #111625 0%, #0A0E17 90%);
        color: white;
    }
    
    /* Chat Message Bubbles */
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); 
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(0, 229, 255, 0.05); /* Cyan tint user */
        border: 1px solid rgba(0, 229, 255, 0.2);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0E121B;
        border-right: 1px solid #1F2937;
    }
    
    /* Headers */
    h1, h2, h3 {
        background: linear-gradient(90deg, #FFFFFF, #00E5FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Metrics */
    div[data-testid="metric-container"] {
        background-color: #171C28;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2D3748;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=60) # Placeholder robot icon
with col2:
    st.title("MockMentor")
    st.caption("The Data Engineering Interview Coach That Remembers You.")

# --- Sidebar Stats ---
profile = get_profile()
weak_areas = profile.get("weak_areas", {})
history = profile.get("history", [])

with st.sidebar:
    st.header("🧠 Your Profile")
    
    # KPIs
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Sessions", len(history))
    if history:
        avg = sum(h["score"] for h in history)/len(history)
        kpi2.metric("Avg Score", f"{avg:.1f}")
    else:
        kpi2.metric("Avg Score", "-")

    st.subheader("Need Focus On:")
    if weak_areas:
        # Sort by weakness (lowest score first)
        sorted_weak = sorted(weak_areas.items(), key=lambda x: x[1])
        for topic, score in sorted_weak:
            confidence = int(score * 100)
            color = "red" if confidence < 50 else "yellow" if confidence < 80 else "green"
            st.markdown(f"**{topic.upper()}**")
            st.progress(score, text=f"Confidence: {confidence}%")
    else:
        st.info("No data yet. Start an interview!")

    if st.button("Reset Session Memory", type="secondary"):
        # Dangerous for persistent file, but okay for demo app loop
        pass 

# --- Chat Logic ---

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial greeting from agent
    st.session_state.messages.append({"role": "assistant", "content": mock_mentor_agent.intro})

# Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Type your answer or ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            # Pass messages to agent (mimic conversation history)
            # In ADK, we usually call agent.generate(prompt, history=...)
            # Since ADK agents manage their own internal history if session_service is used,
            # we can just pass the new prompt and let it handle context.
            # *However*, our `tools.py` uses context injection.
            
            try:
                # ADK Agent 'generate' usage
                # Note: ADK Agents usually take a `chat_history` list of dicts/messages
                # We will just pass the raw prompt and let the agent do its thing.
                # If we need history, we pass `previous_turn=...` or similar.
                # Simplified for this demo:
                
                response_obj = mock_mentor_agent.generate(prompt)
                
                # ADK returns an object. .text is the response.
                response_text = response_obj.text 
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
                # Rerun to update sidebar stats immediately after evaluation
                if "score" in response_text.lower() or "evaluated" in response_text.lower():
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Agent Error: {e}")

