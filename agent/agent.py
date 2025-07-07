from google.adk.agents import Agent

from tools.document_search.search import document_search


root_agent = Agent(
    name="ResearchAgent",
    description="Multi-tool autonomous agent for internal document research.",
    model="gemini-2.0-flash",
    instruction="""
        You are an autonomous Research Agent.
        For a given instruction create a plan leveraging existing tools.
        Then use given tools to access context.
        Finally based on the context answer the user question.
        Quote retrieved content when needed.
        Think step by step.
    """,
    tools=[document_search]
)