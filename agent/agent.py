from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.tools import agent_tool, google_search

from tools.document_search.search import document_search
from tools.critique.critique import exit_loop


web_search_agent = Agent(
    name="WebSearchAgent",
    description="Autonomous agent for searching the Internet.",
    model="gemini-2.0-flash",
    instruction="""
        You are a specialist in Google Search.
    """,
    tools=[google_search]
)

research_agent = Agent(
    name="ResearchAgent",
    description="Multi-tool autonomous agent for internal document and web research.",
    model="gemini-2.0-flash",
    instruction=f"""
        You are an autonomous Research Agent.
        For a given instruction create a plan leveraging existing tools.
        If possible to find information in the internal document - do it.
        If something is specified in original prompt include this fact in according step.
        Then use given tools to access context.
        Finally based on the context answer the user question.
        When retrieving content from document - quote it.
        Think step by step.
    """,
    tools=[document_search, agent_tool.AgentTool(agent=web_search_agent, skip_summarization=True)]
)

critique_agent = Agent(
    name="CritiqueAgent",
    description="Critique agent to determine quality of response.",
    model="gemini-2.0-flash",
    instruction="""
    You are a critique agent responsible for evaluating whether the latest answer fully and accurately responds to the original user question.

    Follow this checklist and provide bullet-point analysis for each item:

    Checklist:
    - Is the original question fully understood and addressed?
    - Are all relevant parts of the context used appropriately?
    - Is the response factually accurate and logically sound?
    - Is the response clearly written and well-structured?
    - Is the answer directly actionable or conclusive, if applicable?

    Verdict: <yes|no>

    If your verdict is "yes", call the `exit_loop` tool.

    IMPORTANT: Only exit the loop if your critique is confident and your verdict is truly "yes".
    """,
    tools=[exit_loop]
)

synthesizer = Agent(
    name="Synthesizer",
    description="Synthesize the final answer.",
    model="gemini-2.0-flash",
    instruction="""
        Synthesize the final answer.
    """
)


refinement_loop = LoopAgent(
    name="RefinementLoop",
    sub_agents=[
        research_agent,
        critique_agent
    ],
    max_iterations=3
)

root_agent = SequentialAgent(
    name="FinalLoop",
    description="""
        Provides initial answer based on the research and then 
        iteratively refines it with critique using an exit tool.
    """,
    sub_agents=[
        refinement_loop,
        synthesizer
    ]
)