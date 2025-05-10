from tools.event_details.main import get_events_from_calendar
from swarm import Agent
from agents_worker.instructions import EVENT_DETAILS_AGENT_INSTRUCTIONS

def to_event_details_agent(context_variables, get_events_from_calendar):
    """
    Transfers control to the Event Details Agent which handles retrieving and processing calendar event information.
    This is typically the first agent called in the booking flow to gather available event types and durations.

    The Event Details Agent is responsible for:
    - Retrieving all available calendar events using the provided API key
    - Determining available appointment types (e.g., 15-min, 30-min consultations)
    - Providing event metadata needed for subsequent booking steps

    Args:
        context_variables (dict): A dictionary containing necessary context information including:
            - calendar_api_key (str): API key required for accessing calendar events
            - Additional parameters may be included for filtering or customizing event retrieval
        get_events_from_calendar (function): A function that retrieves all available calendar events using the provided API key. You must call this function.
    Returns:
        Agent: Returns the event_details_agent instance that handles calendar event retrieval
              using the get_events_from_calendar function

    Note:
        - This agent must be called before checking availability or making bookings
        - The retrieved event details are essential for the entire booking workflow
        - Successful execution is required to proceed with availability checking
    """
    print("Transferring to event details with api key: ", context_variables["calendar_api_key"])
    return event_details_agent



event_details_agent = Agent(
    name = "Event Details Agent",
    instructions = EVENT_DETAILS_AGENT_INSTRUCTIONS,
    parallel_tool_calls=True,
)

event_details_agent.functions = [get_events_from_calendar]

print("\n\n Event details agent: ", event_details_agent.name)
