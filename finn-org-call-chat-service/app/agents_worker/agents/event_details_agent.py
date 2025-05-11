from tools.event_details.main import get_events_from_calendar
from agents_worker.agents.check_availability_agent import to_check_availability_agent
from agents_worker.agents.reserve_slot_agent import to_reserve_slot_agent
from agents_worker.agents.book_appointment_agent import to_book_appointment_agent
from swarm import Agent
from agents_worker.instructions import EVENT_DETAILS_AGENT_INSTRUCTIONS

def to_event_details_agent(context_variables, get_events_from_calendar=None, to_check_availability_agent=None, to_reserve_slot_agent=None, to_book_appointment_agent=None):
    """
    Transfer control to the Event Details Agent to get the event details.
    Args:
        context_variables (dict): A dictionary containing booking context information including:
            - calendar_api_key (str): API key for Cal.com authentication
            - event_id (int, optional): The identifier of the event type being booked
            - slotStart (str, optional): The start time of the slot to be booked
        get_events_from_calendar (callable, optional): Function to get events from calendar. Defaults to None.
        to_check_availability_agent (callable, optional): Function to check availability. Defaults to None.
        to_reserve_slot_agent (callable, optional): Function to reserve slot. Defaults to None.
        to_book_appointment_agent (callable, optional): Function to book appointment. Defaults to None.
    """
    print("Transferring to event details with api key: ", context_variables["calendar_api_key"])
    return event_details_agent



event_details_agent = Agent(
    name = "Event Details Agent",
    instructions = EVENT_DETAILS_AGENT_INSTRUCTIONS,
    parallel_tool_calls=True,
)

event_details_agent.functions = [get_events_from_calendar, to_check_availability_agent, to_reserve_slot_agent, to_book_appointment_agent]

print("\n\n Event details agent: ", event_details_agent.name)
