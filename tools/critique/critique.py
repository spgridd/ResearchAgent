from pydantic import BaseModel
from typing import Literal
from google.genai import types
from google.adk.tools.tool_context import ToolContext

from utils.client import get_client
from utils.prompts import get_critique_prompt


class CritiqueSchema(BaseModel):
    verdict: Literal["correct", "incorrect"]

def exit_loop(tool_context: ToolContext):
  """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
  tool_context.actions.escalate = True
  return {}

def critique_tool(query:str, response: str) -> dict:
    """
    Critique given response from the LLM whether it answers original user query.

    Args:
        query: Original query provided by the user.
        response: Final response from the LLM to be evaluated.
    Returns:
        dict: Verdict from the LLM (correct or incorrect).
    """

    client = get_client()

    prompt = f"Original user query:\n{query}\nLLM response:\n{response}"

    contents = []
    contents.append(types.Content(parts=[types.Part(text=prompt)], role='user'))

    config = {
        'system_instruction': get_critique_prompt(),
        'response_schema': CritiqueSchema,
        'response_mime_type': 'application/json'
    }

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        config=config,
        contents=contents
    )

    return response.candidates[0].content.parts[0].text.strip()

