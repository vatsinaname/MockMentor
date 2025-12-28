"""
MockMentor V2 - Main App
Multi-page Streamlit application with onboarding, match analysis, and interview modes
"""

import streamlit as st
import sys
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Handle Streamlit Cloud secrets
try:
    if hasattr(st, 'secrets'):
        for key in ['MODEL_PROVIDER', 'MODEL_NAME', 'GROQ_API_KEY', 'GOOGLE_API_KEY']:
            if key in st.secrets:
                os.environ[key] = st.secrets[key]
except Exception:
    pass

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Page Config ---
st.set_page_config(
    page_title="MockMentor",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Professional Dark Theme CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    .stApp { background: #0a0a0a; }
    
    #MainMenu, footer { visibility: hidden; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #1f1f23;
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: #1f1f23 !important;
        color: #e4e4e7 !important;
        border: 1px solid #27272a !important;
        font-weight: 500;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #27272a !important;
        border-color: #3f3f46 !important;
        transform: none;
        box-shadow: none;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #fafafa !important;
        font-weight: 600 !important;
    }
    
    p, span, div { color: #a1a1aa; }
    label { color: #d4d4d8 !important; }
    
    /* All buttons - dark/subtle style (no gradients) */
    .stButton > button {
        background: #1f1f23 !important;
        color: #e4e4e7 !important;
        border: 1px solid #27272a !important;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.6rem 1.2rem;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: #27272a !important;
        border-color: #3f3f46 !important;
    }
    
    /* Primary buttons - slightly brighter but still subtle */
    .stButton > button[kind="primary"] {
        background: #27272a !important;
        color: #fafafa !important;
        border: 1px solid #3f3f46 !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #3f3f46 !important;
        border-color: #52525b !important;
    }
    
    /* Text inputs */
    .stTextArea textarea, .stTextInput input {
        background: #18181b !important;
        border: 1px solid #27272a !important;
        color: #fafafa !important;
        border-radius: 8px;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 12px;
    }
    
    [data-testid="stFileUploader"] section {
        padding: 1rem;
    }
    
    [data-testid="stFileUploader"] button {
        background: #27272a !important;
        color: #e4e4e7 !important;
        border: 1px solid #3f3f46 !important;
    }
    
    /* Cards and containers */
    .card {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Match score */
    .match-score {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Skill tags */
    .skill-tag {
        display: inline-block;
        padding: 4px 12px;
        margin: 4px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
    }
    
    .skill-match { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
    .skill-gap { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    
    /* Progress bar */
    .progress-bar {
        height: 8px;
        background: #27272a;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #6366f1);
        border-radius: 4px;
        transition: width 0.3s;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #fafafa !important;
    }
    
    /* Section headers */
    .section-title {
        color: #71717a;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    /* Alerts - dark subtle style */
    .stSuccess, .stInfo, .stWarning {
        background: #18181b !important;
        border: 1px solid #27272a !important;
        color: #a1a1aa !important;
    }
    
    .stSuccess p, .stInfo p, .stWarning p {
        color: #d4d4d8 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "page" not in st.session_state:
    st.session_state.page = "onboarding"

if "resume_data" not in st.session_state:
    st.session_state.resume_data = None

if "jd_data" not in st.session_state:
    st.session_state.jd_data = None

if "match_result" not in st.session_state:
    st.session_state.match_result = None

if "interview_plan" not in st.session_state:
    st.session_state.interview_plan = None


def navigate_to(page: str):
    """Navigate to a different page."""
    st.session_state.page = page
    st.rerun()


# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("## MockMentor")
    st.markdown("*AI Interview Coach*")
    st.markdown("---")
    
    # Navigation - no emojis, clean labels
    pages = {
        "onboarding": "Setup",
        "match": "Match Analysis",
        "interview": "Interview",
        "report": "Report"
    }
    
    for page_id, page_name in pages.items():
        if st.button(page_name, key=f"nav_{page_id}", use_container_width=True):
            navigate_to(page_id)
    
    st.markdown("---")
    
    # Status indicators
    if st.session_state.resume_data:
        st.success("Resume loaded")
    if st.session_state.jd_data:
        st.success("JD analyzed")
    if st.session_state.match_result:
        score = st.session_state.match_result.get("overall_score", 0)
        st.info(f"Match: {score:.0f}%")


# --- Page Router ---
page = st.session_state.page

if page == "onboarding":
    st.markdown("# Welcome to MockMentor")
    st.markdown("Upload your resume and job description to get started with personalized interview prep.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Your Resume")
        uploaded_file = st.file_uploader(
            "Upload PDF or DOCX",
            type=["pdf", "docx", "doc"],
            key="resume_upload"
        )
        
        if uploaded_file:
            with st.spinner("Parsing resume..."):
                try:
                    from mockmentor.resume_parser import parse_resume
                    
                    file_bytes = uploaded_file.read()
                    st.session_state.resume_data = parse_resume(file_bytes, uploaded_file.name)
                    st.success(f"Parsed: {st.session_state.resume_data.get('name', 'Resume')}")
                    
                    skills = st.session_state.resume_data.get("skills", [])[:10]
                    if skills:
                        st.markdown("**Skills detected:** " + ", ".join(skills))
                except Exception as e:
                    st.error(f"Failed to parse: {e}")
    
    with col2:
        st.markdown("### Job Description")
        jd_text = st.text_area(
            "Paste the job description here",
            height=300,
            key="jd_input",
            placeholder="Paste the full job description..."
        )
        
        if jd_text and st.button("Analyze JD", key="analyze_jd"):
            with st.spinner("Analyzing job description..."):
                try:
                    from mockmentor.jd_analyzer import analyze_jd
                    
                    st.session_state.jd_data = analyze_jd(jd_text)
                    st.success(f"Analyzed: {st.session_state.jd_data.get('title', 'Position')}")
                    
                    skills = st.session_state.jd_data.get("required_skills", [])[:8]
                    if skills:
                        st.markdown("**Required skills:** " + ", ".join(skills))
                except Exception as e:
                    st.error(f"Failed to analyze: {e}")
    
    st.markdown("---")
    
    if st.session_state.resume_data and st.session_state.jd_data:
        if st.button("Calculate Match Score", type="primary", use_container_width=True):
            with st.spinner("Calculating match..."):
                try:
                    from mockmentor.match_engine import analyze_match
                    
                    st.session_state.match_result = analyze_match(
                        st.session_state.resume_data,
                        st.session_state.jd_data
                    )
                    navigate_to("match")
                except Exception as e:
                    st.error(f"Match calculation failed: {e}")


elif page == "match":
    if not st.session_state.match_result:
        st.warning("Please complete the setup first.")
        if st.button("← Go to Setup"):
            navigate_to("onboarding")
    else:
        match = st.session_state.match_result
        
        st.markdown("# Match Analysis")
        
        # Big score display
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            score = match.get("overall_score", 0)
            st.markdown(f'<div style="text-align: center;"><span class="match-score">{score:.0f}%</span></div>', unsafe_allow_html=True)
            st.markdown(f'<p style="text-align: center; color: #71717a;">{match.get("recommendation", "")}</p>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Skills breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Matching Skills")
            matched = match.get("skill_match", {}).get("matched_required", [])
            if matched:
                for skill in matched[:8]:
                    st.markdown(f'<span class="skill-tag skill-match">{skill}</span>', unsafe_allow_html=True)
            else:
                st.info("Upload resume to see matches")
        
        with col2:
            st.markdown("### Skills to Focus")
            gaps = match.get("skill_match", {}).get("missing_required", [])
            if gaps:
                for skill in gaps[:8]:
                    st.markdown(f'<span class="skill-tag skill-gap">{skill}</span>', unsafe_allow_html=True)
            else:
                st.success("No major gaps identified!")
        
        st.markdown("---")
        
        # Interview focus areas
        st.markdown("### Interview Focus Areas")
        focus = match.get("interview_focus_areas", [])
        if focus:
            for i, area in enumerate(focus[:5], 1):
                st.markdown(f"{i}. {area}")
        
        st.markdown("---")
        
        # Interview options
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Start Text Interview", type="primary", use_container_width=True):
                with st.spinner("Generating personalized questions..."):
                    try:
                        from mockmentor.question_gen import generate_interview_plan
                        
                        st.session_state.interview_plan = generate_interview_plan(
                            st.session_state.jd_data,
                            st.session_state.resume_data,
                            st.session_state.match_result,
                            num_questions=15
                        )
                        navigate_to("interview")
                    except Exception as e:
                        st.error(f"Failed to generate questions: {e}")
        
        with col2:
            if st.button("Start Voice Interview", use_container_width=True):
                with st.spinner("Generating personalized questions..."):
                    try:
                        from mockmentor.question_gen import generate_interview_plan
                        
                        st.session_state.interview_plan = generate_interview_plan(
                            st.session_state.jd_data,
                            st.session_state.resume_data,
                            st.session_state.match_result,
                            num_questions=15
                        )
                        st.switch_page("pages/voice_interview.py")
                    except Exception as e:
                        st.error(f"Failed to generate questions: {e}")


elif page == "interview":
    if not st.session_state.interview_plan:
        st.warning("Please complete match analysis first.")
        if st.button("← Go to Match"):
            navigate_to("match")
    else:
        from mockmentor.interview_session import get_session
        
        session = get_session()
        
        # Initialize interview if needed
        if not session.interview_plan:
            session.start_interview(
                st.session_state.resume_data,
                st.session_state.jd_data,
                st.session_state.match_result,
                st.session_state.interview_plan
            )
        
        # Import persona
        from mockmentor.persona import (
            get_interviewer_info, 
            format_question_conversationally,
            get_greeting
        )
        
        interviewer = get_interviewer_info()
        
        # Header with interviewer info
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{interviewer['avatar']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**{interviewer['name']}**")
            st.markdown(f"<span style='color: #71717a; font-size: 0.9rem;'>{interviewer['title']}</span>", unsafe_allow_html=True)
        
        # Progress bar
        progress = session.get_progress()
        st.markdown(f'''
            <div style="margin: 1rem 0;">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress['percentage']}%"></div>
                </div>
                <p style="color: #71717a; font-size: 0.8rem; margin-top: 0.5rem;">Question {progress['current']} of {progress['total']}</p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Mode toggle
        col1, col2, _ = st.columns([1, 1, 3])
        with col1:
            if st.button("Text Mode", type="secondary" if session.mode != "text" else "primary"):
                session.mode = "text"
                st.rerun()
        with col2:
            if st.button("Voice Mode", type="secondary" if session.mode != "voice" else "primary"):
                session.mode = "voice"
                st.rerun()
        
        st.markdown("---")
        
        # Current question with conversational framing
        question = session.get_current_question()
        
        if question:
            # Get previous answer for context
            prev_answer = session.answers[-1].get("answer") if session.answers else None
            
            # Format question conversationally
            conversational_text = format_question_conversationally(
                question,
                question_num=session.current_question_idx,
                total=progress['total'],
                previous_answer=prev_answer
            )
            
            # Display as interviewer speech
            st.markdown(f'''
                <div style="background: #18181b; border: 1px solid #27272a; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;">
                    <p style="color: #a1a1aa; font-size: 0.8rem; margin-bottom: 0.5rem;">Topic: {question.get('topic', 'General')}</p>
                    <p style="color: #fafafa; font-size: 1.1rem; line-height: 1.6;">{conversational_text}</p>
                </div>
            ''', unsafe_allow_html=True)
            
            # TTS option for voice mode
            if session.mode == "voice":
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button("Play Question"):
                        try:
                            from mockmentor.voice_engine import synthesize_speech, get_audio_html
                            audio = synthesize_speech(conversational_text)
                            st.markdown(get_audio_html(audio), unsafe_allow_html=True)
                        except Exception as e:
                            st.warning(f"TTS not available: {e}")
            
            if session.mode == "voice":
                st.info("Voice mode: Record your answer using the microphone.")
                try:
                    from audio_recorder_streamlit import audio_recorder
                    
                    audio_bytes = audio_recorder(
                        pause_threshold=2.0,
                        sample_rate=16000,
                        text="Click to record",
                        icon_size="2x"
                    )
                    
                    if audio_bytes:
                        with st.spinner("Transcribing..."):
                            from mockmentor.voice_engine import transcribe_audio_groq, analyze_voice_metrics
                            
                            transcription = transcribe_audio_groq(audio_bytes)
                            st.markdown(f"**Your answer:** {transcription}")
                            
                            # Store for processing
                            st.session_state.current_answer = transcription
                            st.session_state.current_voice_metrics = analyze_voice_metrics(transcription)
                
                except ImportError:
                    st.warning("Voice recording requires `audio-recorder-streamlit`. Using text mode.")
                    session.mode = "text"
                    st.rerun()
            
            # Text input (always available)
            answer = st.text_area(
                "Your answer:",
                value=st.session_state.get("current_answer", ""),
                height=150,
                key="answer_input"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Submit Answer", type="primary", use_container_width=True):
                    if answer:
                        with st.spinner("Evaluating..."):
                            from mockmentor.tools import evaluate_response
                            
                            # Evaluate answer
                            result = evaluate_response(question.get("id", "custom"), answer)
                            score = result.get("overall_score", 5)
                            feedback = result.get("feedback", "Good effort!")
                            
                            # Record answer
                            voice_metrics = st.session_state.get("current_voice_metrics")
                            session.record_answer(answer, score, feedback, voice_metrics)
                            
                            # Show feedback
                            st.markdown(f"**Score:** {score}/10")
                            st.markdown(f"**Feedback:** {feedback}")
                            
                            # Clear for next
                            st.session_state.current_answer = ""
                            st.session_state.current_voice_metrics = None
                    else:
                        st.warning("Please provide an answer.")
            
            with col2:
                if st.button("Next Question →", use_container_width=True):
                    session.advance_question()
                    st.session_state.current_answer = ""
                    st.rerun()
        
        else:
            st.success("Interview complete!")
            if st.button("View Report", type="primary"):
                navigate_to("report")


elif page == "report":
    from mockmentor.interview_session import get_session
    
    session = get_session()
    
    if not session.answers:
        st.warning("Complete an interview to see your report.")
        if st.button("← Start Interview"):
            navigate_to("interview")
    else:
        report = session.generate_final_report()
        
        st.markdown("# Interview Report")
        
        # Overall score
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Score", f"{report.get('overall_score', 0):.0f}/100")
        with col2:
            st.metric("Questions Answered", report.get("questions_answered", 0))
        with col3:
            st.metric("Duration", f"{report.get('duration_minutes', 0):.0f} min")
        
        st.markdown("---")
        
        # Topic breakdown
        st.markdown("### Topic Performance")
        for topic, score in report.get("topic_breakdown", {}).items():
            st.markdown(f"**{topic}:** {score:.1f}/10")
            st.progress(score / 10)
        
        # Voice analysis if available
        if report.get("voice_analysis"):
            st.markdown("---")
            st.markdown("### Voice Analysis")
            voice = report["voice_analysis"]
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Words Spoken", voice.get("total_words_spoken", 0))
                st.metric("Fluency Rating", voice.get("fluency_rating", "N/A"))
            with col2:
                st.metric("Filler Words", voice.get("total_filler_words", 0))
                st.metric("Filler Ratio", f"{voice.get('filler_ratio', 0)}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Interview"):
                from mockmentor.interview_session import reset_session
                reset_session()
                st.session_state.interview_plan = None
                navigate_to("onboarding")
        with col2:
            if st.button("Back to Match"):
                navigate_to("match")
