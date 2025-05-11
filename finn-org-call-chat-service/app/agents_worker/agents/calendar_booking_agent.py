from tools.reserve_slot.main import reserve_slot_for_startTime
from tools.book_appointment.main import book_appointment_for_startTime
from tools.event_details.main import get_events_from_calendar
from tools.check_availability.main import check_all_availabile_slots
from swarm import Agent
from agents_worker.instructions import BOOK_APPOINTMENT_AGENT_INSTRUCTIONS

def to_calendar_booking_agent(context_variables: dict, reserve_slot_for_startTime=None, book_appointment_for_startTime=None):
    """
    Transfer control to the Calendar Booking Agent to book the appointment.
    Args:
        - context_variables (dict): A dictionary containing booking context information including:
            - calendar_api_key (str): API key for Cal.com authentication
            - event_id (int, optional): The identifier of the event type being booked, it is eventtypes id
            - slotStart (str, optional): The start time of the slot to be booked
            - attendee_details (dict): Information about the person booking the appointment
        get_events_from_calendar (callable, optional): Function to get events from calendar. Defaults to None.
        check_all_availabile_slots (callable, optional): Function to check available slots. Defaults to None.
        reserve_slot_for_startTime (callable, optional): Function to reserve slot. Defaults to None.
        book_appointment_for_startTime (callable, optional): Function to book appointment. Defaults to None.
    """
    print("\n\n Calendar booking agent context variables: ", context_variables)
    return calendar_booking_agent



calendar_booking_agent = Agent(
    name = "Calendar Booking Agent",
    instructions = BOOK_APPOINTMENT_AGENT_INSTRUCTIONS,
    parallel_tool_calls=True,
)

calendar_booking_agent.functions = [reserve_slot_for_startTime, book_appointment_for_startTime, get_events_from_calendar, check_all_availabile_slots]

print("\n\n Calendar booking agent: ", calendar_booking_agent.name)