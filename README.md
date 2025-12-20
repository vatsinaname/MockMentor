# MockMentor

AI-powered Data Engineering Interview Coach built with Google ADK.

## Features

- Realistic interview questions across 5 topics: SQL, Pipelines, Modeling, System Design, Debugging
- AI-powered answer evaluation with detailed feedback
- Progress tracking and weak area identification
- Supports multiple LLM providers (Groq, Gemini)

## Quick Start

### 1. Clone and install

```bash
git clone <your-repo>
cd mockmentor
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and add your API key:

```bash
cp .env.example .env
```

Edit `.env`:

```
MODEL_PROVIDER=groq
MODEL_NAME=moonshotai/kimi-k2-instruct
GROQ_API_KEY=your_key_here
```

Or for Gemini:

```
MODEL_PROVIDER=gemini
MODEL_NAME=gemini-2.5-flash
GOOGLE_API_KEY=your_key_here
```

### 3. Run

```bash
streamlit run ui/app.py
```

## Streamlit Cloud Deployment

### 1. Push to GitHub

Ensure `.env` is in `.gitignore` (it is by default).

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repo
3. Set main file path: `ui/app.py`

### 3. Add Secrets

In your app's Settings > Secrets, add:

```toml
MODEL_PROVIDER = "groq"
MODEL_NAME = "moonshotai/kimi-k2-instruct"
GROQ_API_KEY = "your_groq_api_key"
```

Or for Gemini:

```toml
MODEL_PROVIDER = "gemini"
MODEL_NAME = "gemini-2.5-flash"
GOOGLE_API_KEY = "your_google_api_key"
```

## Supported Models

### Groq (via LiteLLM)

- `moonshotai/kimi-k2-instruct` (recommended)
- `llama-3.3-70b-versatile`
- `qwen/qwen3-32b`

### Gemini

- `gemini-2.5-flash` (recommended)
- `gemini-1.5-pro`

## Project Structure

```
mockmentor/
  agent.py      # Agent configuration
  tools.py      # Interview tools
  prompts.py    # System instructions
  questions.py  # Question bank
  rubrics.py    # Grading rubrics
ui/
  app.py        # Streamlit interface
.streamlit/
  config.toml   # Theme configuration
```
