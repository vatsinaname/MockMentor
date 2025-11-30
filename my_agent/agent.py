from google.adk.agents import Agent, Tool
from google.adk.model import Model
from google.adk.sessions import InMemorySessionService
from .tools.search_tools import search_web, read_url

# Define the model to use
model = Model(model_name="gemini-2.5-flash")

# Configure Session Service (Memory)
# In a production app, use DatabaseSessionService
session_service = InMemorySessionService()

# --- Sub-Agent: Researcher ---
researcher_instruction = """
You are a specialized Researcher Agent. Your goal is to find accurate and relevant technical information.
Use the `search_web` tool to find information and `read_url` to get details from specific pages.
Summarize your findings clearly, citing your sources.
"""

researcher_agent = Agent(
    name="Researcher",
    model=model,
    tools=[search_web, read_url],
    instruction=researcher_instruction
)

# --- Sub-Agent: Writer ---
writer_instruction = """
You are a specialized Technical Writer Agent. Your goal is to take raw information and transform it into high-quality documentation.
Format your output in Markdown.
Use clear headings, code blocks, and bullet points.
Ensure the tone is professional and educational.
"""

writer_agent = Agent(
    name="Writer",
    model=model,
    instruction=writer_instruction
)

# --- Root Agent: Coordinator ---
coordinator_instruction = """
You are the Coordinator Agent for 'InsightArchitect'.
Your goal is to manage the research and writing process to answer the user's request.

1. First, understand the user's topic.
2. Delegate to the `Researcher` agent to gather information.
3. Once you have sufficient information, delegate to the `Writer` agent to create the final documentation.
4. Review the output and present it to the user.

Always ensure the final output is high quality.
"""

root_agent = Agent(
    name="Coordinator",
    model=model,
    sub_agents=[researcher_agent, writer_agent],
    instruction=coordinator_instruction,
    session_service=session_service
)
