from tools.get_workflow.main import get_workflow
from swarm import Agent




def to_get_workflow_agent(context_variables, get_workflow):
    """
    Transfers control to the Get Workflow Agent to retrieve the workflow for the user.
    
    Args:
        context_variables (dict): A dictionary containing necessary context information including:
            - Additional context variables may be required for specific sub-agents
        get_workflow (function): A function that retrieves the workflow for the user. You must call this function.
    Returns:
        Agent: Returns the get_workflow_agent instance that handles the workflow retrieval
               using the get_workflow function.
    Note:
        - This agent must be called before any other agents in the workflow
        - The retrieved workflow is essential for the entire booking workflow
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