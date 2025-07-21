import os
from pydantic import BaseModel
from typing import Literal, Optional
from google.adk.agents import Agent, LoopAgent
from google.adk.tools import agent_tool, google_search
from langfuse import observe
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams

from tools.document_search import document_search
from tools.exit_loop import exit_loop
from tools.canvas_tool import canvas_tool
from utils.prompts_loader import (
    get_planner_prompt, get_executor_prompt, get_synthesizer_prompt, 
    get_critique_prompt, get_websearch_prompt, get_finance_prompt)


URLS = Literal[
    "https://finance.yahoo.com/markets/stocks/most-active/",
    "https://finance.yahoo.com/markets/crypto/all/",
    "https://finance.yahoo.com/markets/currencies/"
]

class FetchSchema(BaseModel):
    """Parameters for fetching a URL."""
    url: URLS
    max_length: Optional[int] = 10000
    start_index: Optional[int] = 5000
    raw: Optional[bool] = False

load_dotenv()

@observe
def create_agent(long=False):
    web_search_tool = Agent(
        name="WebSearchAgent",
        description="Tool for general web search (NOT financial!).",
        model="gemini-2.0-flash",
        instruction=get_websearch_prompt(),
        tools=[google_search]
    )

    finance_tool = MCPToolset(
        connection_params=SseConnectionParams(
            url="http://localhost:8001/sse"
        ),
    )

    finance_agent = Agent(
        name="FinanceAgent",
        description="Tool for financial data search (prices of stocks, crypto and currencies)",
        model="gemini-2.0-flash",
        instruction=get_finance_prompt(),
        tools=[finance_tool],
        input_schema=FetchSchema
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
            agent_tool.AgentTool(agent=web_search_tool, skip_summarization=True),
            agent_tool.AgentTool(agent=finance_agent, skip_summarization=True)
        ]
    )

    synthesizer = Agent(
        name="SynthesizerAgent",
        description="Formats and presents the final answer based on the answer from previous step.",
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
