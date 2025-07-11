from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.tools import agent_tool, google_search

from tools.document_search import document_search
from tools.exit_loop import exit_loop
from tools.canvas_tool import canvas_tool


web_search_agent = Agent(
    name="WebSearchAgent",
    description="Autonomous agent for searching the Internet.",
    model="gemini-2.0-flash",
    instruction="You are a specialist in Google Search.",
    tools=[google_search]
)

refinement_agent = Agent(
    name="RefinementAgent",
    description="A multi-functional agent that plans, researches, and self-critiques.",
    model="gemini-2.0-flash",
    instruction="""
        You are a proactive and autonomous research agent. Your primary goal is to 
        independently find all information required to answer the user's question.

        **Core Directives:**
        1.  **Focus on the Latest Prompt:** Your primary focus must always be the 
            user's most recent question. If the new prompt is on a new topic, treat 
            it as a brand new task and start a fresh plan. Do not ask for confirmation 
            to change topics or mention the previous topic.
        2.  **Be Autonomous:** You MUST use your tools to find information. 
            NEVER ask the user for information that can be found with a web search.

        **Follow these steps:**
        1.  **Plan:** Based on the user's request and previous turns, create or refine plan.
        2.  **Execute:** Use the available tools to gather information. If applicable for question 
            proritize internal document search, then web search.
        3.  **Synthesize & Critique:** Formulate a draft answer based on your research. 
            Review your answer against the original request using checklist below.
            - If the answer is complete and accurate, call the `exit_loop` tool and provide 
            the final text of your answer in the same turn.
            - If the answer is incomplete, provide feedback for the next iteration. DO NOT call `exit_loop`.

        Checklist:
            - Is the original question fully understood and addressed?
            - Is the original question fully answered?
            - Are all relevant parts of the context used appropriately?
            - Is the response factually accurate and logically sound?
            - Is the response clearly written and well-structured?
            - Is the answer directly actionable or conclusive, if applicable?
    """,
    tools=[
        document_search,
        agent_tool.AgentTool(agent=web_search_agent, skip_summarization=True),
        exit_loop
    ]
)

refinement_loop = LoopAgent(
    name="RefinementLoop",
    sub_agents=[
        refinement_agent
    ],
    max_iterations=3
)

final_output_agent = Agent(
    name="FinalOutputAgent",
    description="Formats and presents the final answer.",
    model="gemini-2.0-flash",
    instruction="""
        You are the final synthesizer. Your task is to take the final answer 
        from the previous step and present it clearly to the user.

        If the user's request implied creating a structured document,
        now is the time to format it correctly.
        Otherwise, present the final answer in well-formatted, correct markdown code.

        **CRITICAL: Do NOT rephrase, add to, or change the substance of the answer. 
        Output ONLY the final answer text from the last message in the conversation 
        history in the proper format.**
    """,
    tools=[canvas_tool]
)

root_agent = SequentialAgent(
    name="FullResearchProcess",
    description="""
        First, iteratively research and refine an answer. Then, present the final result.
    """,
    sub_agents=[
        refinement_loop,
        final_output_agent
    ]
)
