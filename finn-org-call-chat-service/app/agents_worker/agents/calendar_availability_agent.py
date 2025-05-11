from tools.check_availability.main import check_all_availabile_slots
from tools.event_details.main import get_events_from_calendar
from swarm import Agent

from agents_worker.instructions import CHECK_AVAILABILITY_AGENT_INSTRUCTIONS

def to_calendar_availability_agent(context_variables, get_events_from_calendar=None, check_all_availabile_slots=None):
    """
    Transfer control to the Check Availability Agent to get the available slots for the event.
    Args:
        context_variables (dict): A dictionary containing booking context information including:
            - event_id (int, optional): The identifier of the event type being booked, it is eventtypes id
            - calendar_api_key (str): API key for Cal.com authentication
            - slotStart (str, optional): The start time of the slot to be booked
            - slotEnd (str, optional): The end time of the slot to be booked
        get_events_from_calendar (callable, optional): Function to get events from calendar. Defaults to None.
        check_all_availabile_slots (callable, optional): Function to check available slots. Defaults to None.
    """
    print("Transferring to check availability with event id: ", context_variables["event_id"])
    return calendar_availability_agent


calendar_availability_agent = Agent(
    name = "Calendar Availability Agent",
    instructions = CHECK_AVAILABILITY_AGENT_INSTRUCTIONS,
    parallel_tool_calls=True,
)

calendar_availability_agent.functions = [get_events_from_calendar, check_all_availabile_slots]

print("\n\n Calendar availability agent: ", calendar_availability_agent.name)