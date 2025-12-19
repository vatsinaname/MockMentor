# MockMentor: The Data Engineering Interview Coach That Remembers You

![MockMentor](https://cdn-icons-png.flaticon.com/512/4712/4712035.png)

**Mock interview tools have no memory. Every session starts from zero.**  
MockMentor solves this. It's an agentic AI coach that tracks your weak areas, adapts to your skill level, and helps you systematically close gaps.

## Features

- Persistent Memory: Remembers your struggle with Window Functions from last week.
- Adaptive Questioning: Selects questions weighted toward your weak areas.
- Detailed Rubrics: Scores every answer on Accuracy, Completeness, and Clarity.
- Futuristic UI: A stunning Interface built with Streamlit.

## Architecture

MockMentor uses the Google ADK (Agent Development Kit) and Gemini 2.0 Flash.

- Agent: Orchestrates the interview flow.
- Tools: `select_question`, `evaluate_response` (grading), `weakness_tracker`.
- Memory: JSON-based persistent session storage (`mockmentor_db.json`).

## Quick Start

1. Install Dependencies

   ```shell
   pip install -r requirements.txt
   ```

2. Set API Key
   Make sure your environment has `GOOGLE_API_KEY` set (or configure `google-adk`).

3. Run the App
   ```shell
   streamlit run ui/app.py
   ```

## Project Structure

- `mockmentor/`: Core agent logic.
  - `questions.py`: Question bank.
  - `rubrics.py`: Grading criteria.
  - `tools.py`: Tool implementations.
  - `agent.py`: Agent configuration.
- `ui/`: Streamlit frontend.
  - `app.py`: Main application entry point.

## Demo

Open the app and say "I want to practice SQL". The agent will guide you from there.
