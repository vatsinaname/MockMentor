"""
Voice Engine
Speech-to-text and text-to-speech for voice interview mode
"""

import os
import asyncio
import tempfile
from typing import Optional, Tuple
import base64


def transcribe_audio_groq(audio_bytes: bytes, filename: str = "audio.wav") -> str:
    """
    Transcribe audio using Groq's Whisper API.
    
    Args:
        audio_bytes: Raw audio file bytes
        filename: Filename for format detection
    
    Returns:
        Transcribed text
    """
    from groq import Groq
    
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set")
    
    client = Groq(api_key=api_key)
    
    # Save to temp file for API
    with tempfile.NamedTemporaryFile(suffix=f".{filename.split('.')[-1]}", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    
    try:
        with open(tmp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(filename, audio_file),
                model="whisper-large-v3",
                response_format="text",
                language="en"
            )
        return transcription.strip()
    finally:
        os.unlink(tmp_path)


async def synthesize_speech_edge(text: str, voice: str = "en-IN-NeerjaNeural") -> bytes:
    """
    Generate speech from text using Edge TTS (free).
    
    Args:
        text: Text to speak
        voice: Voice name (default: natural female US voice)
    
    Returns:
        Audio bytes (MP3 format)
    """
    import edge_tts
    
    communicate = edge_tts.Communicate(text, voice)
    
    audio_chunks = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])
    
    return b"".join(audio_chunks)


def synthesize_speech(text: str, voice: str = "en-IN-NeerjaNeural") -> bytes:
    """
    Synchronous wrapper for speech synthesis.
    
    Args:
        text: Text to speak
        voice: Voice name
    
    Returns:
        Audio bytes (MP3)
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(synthesize_speech_edge(text, voice))


def get_audio_html(audio_bytes: bytes, autoplay: bool = True) -> str:
    """
    Create HTML audio element from audio bytes.
    
    Args:
        audio_bytes: MP3 audio bytes
        autoplay: Whether to autoplay
    
    Returns:
        HTML string with embedded audio
    """
    b64 = base64.b64encode(audio_bytes).decode()
    autoplay_attr = "autoplay" if autoplay else ""
    
    return f'''
    <audio {autoplay_attr} controls style="width: 100%; margin: 10px 0;">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    '''


def analyze_voice_metrics(transcription: str, audio_duration_seconds: float = None) -> dict:
    """
    Analyze voice response for fluency and coherence metrics.
    
    Args:
        transcription: Transcribed text from voice response
        audio_duration_seconds: Duration of audio (if available)
    
    Returns:
        {
            "word_count": int,
            "filler_words": {"count": int, "examples": [str]},
            "speaking_pace": str,
            "estimated_confidence": str,
            "coherence_notes": str
        }
    """
    words = transcription.split()
    word_count = len(words)
    
    # Detect filler words
    filler_patterns = ["um", "uh", "like", "you know", "basically", "actually", "so,", "well,"]
    filler_count = 0
    filler_examples = []
    
    text_lower = transcription.lower()
    for filler in filler_patterns:
        count = text_lower.count(filler)
        if count > 0:
            filler_count += count
            filler_examples.append(f"{filler} ({count}x)")
    
    # Estimate pace if duration available
    if audio_duration_seconds and audio_duration_seconds > 0:
        wpm = (word_count / audio_duration_seconds) * 60
        if wpm < 100:
            pace = "slow"
        elif wpm < 150:
            pace = "normal"
        elif wpm < 180:
            pace = "fast"
        else:
            pace = "very fast"
    else:
        pace = "unknown"
    
    # Estimate confidence based on filler ratio
    filler_ratio = filler_count / word_count if word_count > 0 else 0
    if filler_ratio < 0.02:
        confidence = "high"
    elif filler_ratio < 0.05:
        confidence = "moderate"
    else:
        confidence = "low - consider practicing more"
    
    # Basic coherence check
    sentence_count = transcription.count('.') + transcription.count('!') + transcription.count('?')
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else word_count
    
    if avg_sentence_length > 40:
        coherence = "Long sentences - try to be more concise"
    elif avg_sentence_length < 5:
        coherence = "Very short responses - consider elaborating"
    else:
        coherence = "Good sentence structure"
    
    return {
        "word_count": word_count,
        "filler_words": {
            "count": filler_count,
            "examples": filler_examples[:5]
        },
        "speaking_pace": pace,
        "estimated_confidence": confidence,
        "coherence_notes": coherence
    }


# Available voices for TTS - Indian English
DEFAULT_VOICE = "en-IN-NeerjaNeural"  # Indian English female

AVAILABLE_VOICES = {
    "interviewer_female": "en-IN-NeerjaNeural",  # Indian English female
    "interviewer_male": "en-IN-PrabhatNeural",   # Indian English male
    "interviewer_hindi_f": "hi-IN-SwaraNeural",  # Hindi female
    "interviewer_hindi_m": "hi-IN-MadhurNeural", # Hindi male
}
