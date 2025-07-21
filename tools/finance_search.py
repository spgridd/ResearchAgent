from typing import Literal, Optional
from pydantic import BaseModel
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams
from google.adk.agents import Agent

from utils.prompts_loader import get_finance_prompt


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


mcp_fetch_tool = MCPToolset(
    connection_params=SseConnectionParams(
        url="http://localhost:8001/sse"
    ),
)

finance_tool = Agent(
    name="FinanceAgent",
    description="Tool for financial data search (prices of stocks, crypto and currencies)",
    model="gemini-2.0-flash",
    instruction=get_finance_prompt(),
    tools=[mcp_fetch_tool],
    input_schema=FetchSchema
)
