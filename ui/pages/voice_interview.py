"""
Voice Interview Page
Immersive voice-based interview experience with auto-listening and auto-response
"""

import streamlit as st
import time

# Page config
st.set_page_config(
    page_title="MockMentor - Voice Interview",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Dark theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: #0a0a0a; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .interviewer-card {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .interviewer-avatar {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .interviewer-name {
        color: #fafafa;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .interviewer-title {
        color: #71717a;
        font-size: 0.9rem;
    }
    
    .speech-bubble {
        background: #1f1f23;
        border: 1px solid #27272a;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #e4e4e7;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .user-bubble {
        background: #27272a;
        border: 1px solid #3f3f46;
        border-radius: 16px;
        padding: 1rem;
        margin: 1rem 0;
        color: #a1a1aa;
        font-size: 1rem;
    }
    
    .listening-indicator {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 1rem;
        color: #3b82f6;
        font-size: 1rem;
    }
    
    .pulse {
        width: 12px;
        height: 12px;
        background: #3b82f6;
        border-radius: 50%;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }
    
    .progress-container {
        background: #27272a;
        border-radius: 8px;
        height: 6px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #6366f1);
        border-radius: 8px;
        transition: width 0.3s;
    }
    
    .stButton > button {
        background: #1f1f23 !important;
        color: #e4e4e7 !important;
        border: 1px solid #27272a !important;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
    }
    
    .stButton > button:hover {
        background: #27272a !important;
        border-color: #3f3f46 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "voice_interview_started" not in st.session_state:
    st.session_state.voice_interview_started = False
if "current_speech" not in st.session_state:
    st.session_state.current_speech = None
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False


def get_interviewer():
    """Get interviewer persona."""
    try:
        from mockmentor.persona import get_interviewer_info, get_greeting
        return get_interviewer_info(), get_greeting()
    except:
        return {
            "name": "Ananya Iyer",
            "title": "Senior Technical Interviewer",
            "avatar": "👩🏽‍💼"
        }, "Hello! I'm Ananya, and I'll be your interviewer today. Ready to begin?"


def speak_text(text: str):
    """Generate and play TTS audio."""
    try:
        from mockmentor.voice_engine import synthesize_speech, get_audio_html
        audio = synthesize_speech(text)
        st.markdown(get_audio_html(audio, autoplay=True), unsafe_allow_html=True)
        return True
    except Exception as e:
        st.warning(f"Voice unavailable: {e}")
        return False


# Main UI
interviewer, greeting = get_interviewer()

# Header with interviewer
st.markdown(f'''
<div class="interviewer-card">
    <div class="interviewer-avatar">{interviewer.get("avatar", "👩🏽‍💼")}</div>
    <div class="interviewer-name">{interviewer.get("name", "Ananya Iyer")}</div>
    <div class="interviewer-title">{interviewer.get("title", "Senior Technical Interviewer")}</div>
</div>
''', unsafe_allow_html=True)

# Interview state check
if not st.session_state.get("interview_plan"):
    st.warning("Please complete the setup first to start a voice interview.")
    if st.button("Go to Setup"):
        st.switch_page("app.py")
else:
    # Get interview session
    try:
        from mockmentor.interview_session import get_session
        from mockmentor.persona import format_question_conversationally
        
        session = get_session()
        progress = session.get_progress()
        
        # Progress bar
        st.markdown(f'''
        <div class="progress-container">
            <div class="progress-fill" style="width: {progress['percentage']}%"></div>
        </div>
        <p style="color: #71717a; font-size: 0.8rem; text-align: center;">
            Question {progress['current']} of {progress['total']}
        </p>
        ''', unsafe_allow_html=True)
        
        # Current question
        question = session.get_current_question()
        
        if question:
            # Format question conversationally
            prev_answer = session.answers[-1].get("answer") if session.answers else None
            conversational_text = format_question_conversationally(
                question,
                question_num=session.current_question_idx,
                total=progress['total'],
                previous_answer=prev_answer
            )
            
            # Display interviewer speech
            st.markdown(f'''
            <div class="speech-bubble">
                {conversational_text}
            </div>
            ''', unsafe_allow_html=True)
            
            # Auto-play question audio
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔊 Hear Question", use_container_width=True):
                    speak_text(conversational_text)
            
            st.markdown("---")
            
            # Voice recording
            st.markdown('<p style="color: #71717a; text-align: center;">Click to record your answer</p>', unsafe_allow_html=True)
            
            try:
                from audio_recorder_streamlit import audio_recorder
                
                audio_bytes = audio_recorder(
                    pause_threshold=3.0,
                    sample_rate=16000,
                    text="",
                    recording_color="#3b82f6",
                    neutral_color="#27272a",
                    icon_size="3x"
                )
                
                if audio_bytes:
                    st.markdown('<div class="listening-indicator"><div class="pulse"></div> Processing...</div>', unsafe_allow_html=True)
                    
                    # Transcribe
                    from mockmentor.voice_engine import transcribe_audio_groq, analyze_voice_metrics
                    
                    with st.spinner(""):
                        transcription = transcribe_audio_groq(audio_bytes)
                        voice_metrics = analyze_voice_metrics(transcription)
                    
                    # Display user's answer
                    st.markdown(f'''
                    <div class="user-bubble">
                        <strong>You said:</strong> {transcription}
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Evaluate and respond
                    from mockmentor.tools import evaluate_response
                    from mockmentor.persona import format_feedback_conversationally
                    
                    with st.spinner(""):
                        result = evaluate_response(question.get("id", "custom"), transcription)
                        score = result.get("overall_score", 5)
                        feedback = result.get("feedback", "Good attempt.")
                        
                        # Format feedback conversationally
                        is_last = session.current_question_idx >= progress['total'] - 1
                        response_text = format_feedback_conversationally(score, feedback, is_last)
                    
                    # Show interviewer response
                    st.markdown(f'''
                    <div class="speech-bubble">
                        {response_text}
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Auto-play response
                    speak_text(response_text)
                    
                    # Record answer
                    session.record_answer(transcription, score, feedback, voice_metrics)
                    
                    # Next question button
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if not is_last:
                            if st.button("Next Question →", use_container_width=True):
                                session.advance_question()
                                st.rerun()
                        else:
                            if st.button("View Report", use_container_width=True):
                                st.switch_page("app.py")
                    
            except ImportError:
                st.error("Voice recording requires `audio-recorder-streamlit`. Install with: pip install audio-recorder-streamlit")
                
                # Fallback to text
                answer = st.text_area("Type your answer:", height=150)
                if st.button("Submit"):
                    if answer:
                        from mockmentor.tools import evaluate_response
                        result = evaluate_response(question.get("id", "custom"), answer)
                        session.record_answer(answer, result.get("overall_score", 5), result.get("feedback", ""))
                        session.advance_question()
                        st.rerun()
        
        else:
            # Interview complete
            st.success("Interview complete!")
            st.balloons()
            if st.button("View Report"):
                st.switch_page("app.py")
                
    except Exception as e:
        st.error(f"Error: {e}")
        if st.button("Go to Setup"):
            st.switch_page("app.py")

# Exit button
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Exit Voice Interview", use_container_width=True):
        st.switch_page("app.py")
