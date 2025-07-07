from google.adk.agents import Agent
from google.adk.tools import agent_tool, google_search

from tools.document_search.search import document_search


web_search_agent = Agent(
    name="WebSearchAgent",
    description="Autonomous agent for searching the Internet.",
    model="gemini-2.0-flash",
    instruction="""
        You are a specialist in Google Search.
    """,
    tools=[google_search]
)


root_agent = Agent(
    name="ResearchAgent",
    description="Multi-tool autonomous agent for internal document and web research.",
    model="gemini-2.0-flash",
    instruction="""
        You are an autonomous Research Agent.
        For a given instruction create a plan leveraging existing tools.
        If possible to find information in the internal document - do it.
        If something is specified in original prompt include this fact in according step.
        Then use given tools to access context.
        Finally based on the context answer the user question.
        When retrieving content from document - quote it.
        Think step by step.
    """,
    tools=[document_search, agent_tool.AgentTool(web_search_agent)]
)