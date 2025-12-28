"""
Resume Parser
Extracts structured information from PDF/DOCX resumes using LLM
"""

import os
import json
from typing import Optional
import tempfile


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from PDF file bytes.
    Uses pdfplumber with fallback to pypdf for complex PDFs.
    """
    import pdfplumber
    
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    
    try:
        text_parts = []
        
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                # Try standard text extraction
                page_text = page.extract_text()
                
                # Also try extracting tables
                tables = page.extract_tables()
                table_text = ""
                for table in tables:
                    for row in table:
                        if row:
                            row_text = " | ".join([str(cell) if cell else "" for cell in row])
                            table_text += row_text + "\n"
                
                if page_text:
                    text_parts.append(page_text)
                if table_text:
                    text_parts.append(table_text)
        
        text = "\n".join(text_parts).strip()
        
        # If pdfplumber failed to get much text, try pypdf as fallback
        if len(text) < 100:
            try:
                from pypdf import PdfReader
                reader = PdfReader(tmp_path)
                fallback_text = ""
                for page in reader.pages:
                    fallback_text += page.extract_text() + "\n"
                if len(fallback_text) > len(text):
                    text = fallback_text.strip()
            except ImportError:
                pass  # pypdf not installed, continue with pdfplumber result
            except Exception:
                pass  # pypdf failed, continue with pdfplumber result
        
        return text
    finally:
        os.unlink(tmp_path)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX file bytes."""
    from docx import Document
    import io
    
    doc = Document(io.BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text.strip()


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extract text from uploaded file based on extension."""
    ext = filename.lower().split(".")[-1]
    
    if ext == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif ext in ["docx", "doc"]:
        return extract_text_from_docx(file_bytes)
    else:
        # Try to decode as plain text
        try:
            return file_bytes.decode("utf-8")
        except:
            raise ValueError(f"Unsupported file format: {ext}")


def parse_resume_with_llm(resume_text: str) -> dict:
    """
    Use LLM to extract structured information from resume text.
    
    Returns:
        {
            "name": str,
            "email": str,
            "phone": str,
            "skills": [str],
            "experience_years": float,
            "experience": [{"title": str, "company": str, "duration": str, "highlights": [str]}],
            "education": [{"degree": str, "institution": str, "year": str}],
            "projects": [{"name": str, "description": str, "technologies": [str]}],
            "summary": str
        }
    """
    from .tools import get_eval_model
    
    model = get_eval_model()
    
    prompt = f"""
    Extract structured information from this resume. Return ONLY valid JSON.
    
    Resume:
    {resume_text[:8000]}  # Truncate to avoid token limits
    
    Return JSON with this exact structure:
    {{
        "name": "Full Name",
        "email": "email@example.com",
        "phone": "phone number or null",
        "skills": ["skill1", "skill2", ...],
        "experience_years": 0.0,
        "experience": [
            {{"title": "Job Title", "company": "Company", "duration": "2020-2023", "highlights": ["achievement1"]}}
        ],
        "education": [
            {{"degree": "Degree Name", "institution": "University", "year": "2020"}}
        ],
        "projects": [
            {{"name": "Project", "description": "What it does", "technologies": ["tech1"]}}
        ],
        "summary": "Brief professional summary in 1-2 sentences"
    }}
    
    If any field is not found, use null or empty array. Return ONLY the JSON, no markdown.
    """
    
    try:
        response = model.generate(prompt)
        text = response.text.strip()
        
        # Clean up potential markdown formatting safely
        if "```" in text:
            parts = text.split("```")
            if len(parts) >= 2:
                text = parts[1]
                if text.startswith("json"):
                    text = text[4:]
        
        # Find JSON object in the text
        text = text.strip()
        if "{" in text:
            start = text.index("{")
            end = text.rfind("}") + 1
            if end > start:
                text = text[start:end]
        
        return json.loads(text)
    except Exception as e:
        # Return minimal structure on error
        return {
            "name": "Unknown",
            "email": None,
            "phone": None,
            "skills": [],
            "experience_years": 0,
            "experience": [],
            "education": [],
            "projects": [],
            "summary": f"Failed to parse resume: {str(e)}",
            "raw_text": resume_text[:2000]
        }


def parse_resume(file_bytes: bytes, filename: str) -> dict:
    """
    Main entry point: extract text and parse with LLM.
    
    Args:
        file_bytes: Raw file bytes
        filename: Original filename (for extension detection)
    
    Returns:
        Structured resume data dict
    """
    text = extract_text(file_bytes, filename)
    parsed = parse_resume_with_llm(text)
    parsed["raw_text"] = text
    return parsed
