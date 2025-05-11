from tools.get_workflow.main import get_workflow
from swarm import Agent




def to_get_workflow_agent(context_variables, get_workflow=None):
    """
    Transfers control to the Get Workflow Agent to retrieve the workflow for the user.
    Args:
        context_variables (dict): A dictionary containing booking context information.
        get_workflow (callable, optional): Function to get workflow. Defaults to None.
    """
    print("Transferring to get workflow")
    return get_workflow_agent



get_workflow_agent = Agent(
    name = "Get Workflow Agent",
    instructions = "You have to get the workflow for the user",
    parallel_tool_calls=True,
)

get_workflow_agent.functions = [get_workflow]

print("\n\n Get workflow agent: ", get_workflow_agent.name)