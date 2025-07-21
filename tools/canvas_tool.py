from typing import Literal, Dict, Any
from jinja2 import Template
from langfuse import observe

@observe
def canvas_tool(
    format: Literal["markdown", "html", "python", "text"],
    content: Dict[str, Any],
    template: str = ""
) -> str:
    """
    Generates a formatted output (text, markdown, html, or code) using structured content and optional template.

    Args:
        format: The target format for output.
        content: Structured content to populate into the template.
        template: Optional Jinja2 template. If not provided, a default will be used based on format.
    Returns:
        str: Properly formatted output.
    """

    default_templates = {
        "markdown": "# {{ title }}\n\n{{ body }}",
        "html": "<html><body><h1>{{ title }}</h1><p>{{ body }}</p></body></html>",
        "python": "# {{ title }}\n\n{{ body }}",
        "text": "{{ title }}\n\n{{ body }}"
    }

    if not template:
        template = default_templates.get(format, "{{ title }}\n\n{{ body }}")

    try:
        rendered = Template(template).render(**content)
        return rendered
    except Exception as e:
        return f"Error rendering template: {str(e)}"
