from google.adk.agents import Agent
from google.adk.tools import google_search

from utils.prompts_loader import get_websearch_prompt


web_search_tool = Agent(
    name="WebSearchAgent",
    description="Tool for general web search (NOT financial!).",
    model="gemini-2.0-flash",
    instruction=get_websearch_prompt(),
    tools=[google_search]
)
