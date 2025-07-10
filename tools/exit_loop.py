from google.adk.tools.tool_context import ToolContext

def exit_loop(tool_context: ToolContext):
    """
    Call this function ONLY when the critique indicates no further changes 
    are needed, signaling the iterative process should end.
    """
    tool_context.actions.escalate = True

    return {}  
