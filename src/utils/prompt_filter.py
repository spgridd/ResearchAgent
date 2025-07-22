from typing import Literal, Optional
from pydantic import BaseModel
import json
from google.genai import types

from utils.client import get_client
from utils.prompts_loader import get_filter_prompt


class FilterSchema(BaseModel):
    content_type: Literal["table", "text", "image", "any"]
    greater_than: Optional[int]
    less_than: Optional[int]


def extract_filters(prompt):
    client = get_client()

    contents = []
    contents.append(types.Content(parts=[types.Part(text=prompt)], role='user'))

    config = {
        "system_instruction": get_filter_prompt(),
        "temperature": 0.0,
        "response_schema": FilterSchema,
        "response_mime_type": "application/json"
    }

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=contents,
        config=config
    )

    return response.candidates[0].content.parts[0].text.strip()


def get_faiss_filter(filters, force_content_type=None):
    """
    Generates a FAISS metadata filter.
    
    Can now be forced to generate a filter for a specific content type while
    preserving other extracted filters from the user_prompt.
    """

    try:
        filters_dict = json.loads(filters)
    except json.JSONDecodeError:
        filters_dict = {}

    content_type = force_content_type if force_content_type else filters_dict.get("content_type", "any")
    
    any_flag = (content_type == "any")

    greater_than = filters_dict.get("greater_than")
    less_than = filters_dict.get("less_than")

    faiss_filter_dict = {}
    if not any_flag:
        faiss_filter_dict["content_type"] = content_type

    if greater_than is not None or less_than is not None:
        def page_number_filter(metadata):
            type_match = True
            if not any_flag:
                type_match = metadata.get("content_type") == content_type

            page = metadata.get("page_number", 0)
            page_match = (greater_than is None or page > greater_than) and \
                         (less_than is None or page < less_than)
            
            return type_match and page_match
        
        return page_number_filter, (filters_dict.get("content_type") == "any")

    return faiss_filter_dict, any_flag
