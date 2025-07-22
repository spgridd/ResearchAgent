from dotenv import load_dotenv
from google.adk.agents import Agent, LoopAgent
from google.adk.tools import agent_tool
from langfuse import observe

from tools.document_search import document_search
from tools.exit_loop import exit_loop
from tools.canvas import canvas_tool
from tools.web_search import web_search_tool
from tools.finance_search import finance_tool
from utils.prompts_loader import (
    get_planner_prompt, get_executor_prompt, get_synthesizer_prompt, get_critique_prompt
)


load_dotenv()

@observe
def create_agent(long=False):
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
            agent_tool.AgentTool(agent=finance_tool, skip_summarization=True)
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


# For 'adk web' tool usage
root_agent = create_agent()
