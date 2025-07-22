from pathlib import Path
import yaml
from functools import lru_cache
from typing import Any, Dict


PROMPTS_FILE_PATH = Path(__file__).parent.parent / "config/prompts.yaml"


@lru_cache
def load_prompts() -> Dict[str, Any]:
    """
    Load prompts from the YAML configuration file using caching.
    """
    if not PROMPTS_FILE_PATH.exists():
        raise FileNotFoundError(f"Prompts file not found: {PROMPTS_FILE_PATH}")
    
    with PROMPTS_FILE_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def get_websearch_prompt() -> str:
    return load_prompts()["web_search"]


def get_finance_prompt() -> str:
    return load_prompts()["finance"]


def get_planner_prompt(long: bool = False) -> str:
    key = "long" if long else "short"
    return load_prompts()["planner_prompt"][key]


def get_executor_prompt() -> str:
    return load_prompts()["executor_prompt"]


def get_synthesizer_prompt(long: bool = False) -> str:
    key = "long" if long else "short"
    return load_prompts()["synthesizer_prompt"][key]


def get_critique_prompt() -> str:
    return load_prompts()["critique_prompt"]


def get_filter_prompt() -> str:
    return load_prompts()["filter_prompt"]