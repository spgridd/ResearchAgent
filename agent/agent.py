import os
from google.adk.agents import Agent, LoopAgent
from google.adk.tools import agent_tool, google_search
from langfuse.decorators import observe
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, SseConnectionParams

from tools.document_search import document_search
from tools.exit_loop import exit_loop
from tools.canvas_tool import canvas_tool
from utils.prompts_loader import (get_planner_prompt, get_executor_prompt, 
                           get_synthesizer_prompt, get_critique_prompt)


load_dotenv()

@observe
def create_agent(long=False):
    web_search_agent = Agent(
        name="WebSearchAgent",
        description="Autonomous agent for searching the Internet.",
        model="gemini-2.0-flash",
        instruction="You are a specialist in Google Search.",
        tools=[google_search]
    )

    fetch_mcp_toolset = MCPToolset(
        connection_params=SseConnectionParams(
            url="http://localhost:8001/sse"
        ),
    )

    planner = Agent(
        name="PlannerAgent",
        description="An agent for planning whole workflow.",
        model="gemini-2.0-flash",
        instruction=get_planner_prompt(long=long)
    )

    executor = Agent(
        name="ExecutorAgent",
        description="An agent that execute steps of the given plan.",
        model="gemini-2.0-flash",
        instruction=get_executor_prompt(),
        tools=[
            document_search,
            agent_tool.AgentTool(agent=web_search_agent, skip_summarization=True),
            fetch_mcp_toolset
        ]
    )

    synthesizer = Agent(
        name="SynthesizerAgent",
        description="Formats and presents the final answer.",
        model="gemini-2.0-flash",
        instruction=get_synthesizer_prompt(long=long),
        tools=[canvas_tool]
    )

    critique = Agent(
        name="CritiqueAgent",
        description="Critique agent to determine quality of response.",
        model="gemini-2.0-flash",
        instruction=get_critique_prompt(),
        tools=[exit_loop]
    )

    root_agent = LoopAgent(
        name="RefinementLoop",
        sub_agents=[
            planner,
            executor,
            synthesizer,
            critique
        ],
        max_iterations=3
    )

    return root_agent

root_agent = create_agent()
