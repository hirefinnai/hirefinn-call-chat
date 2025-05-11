from agents_worker.agents.calendar_availability_agent import to_calendar_availability_agent
from agents_worker.agents.calendar_booking_agent import to_calendar_booking_agent
from swarm import Agent
from agents_worker.instructions import CALENDAR_AGENT_INSTRUCTIONS

def to_calendar_agent(context_variables, to_calendar_availability_agent=None, to_calendar_booking_agent=None):
    """
    Transfer control to the Calendar Agent to get the event details, check availability, reserve slot and book appointment.
    Args:
        context_variables (dict): A dictionary containing booking context information, subagent context variables.
            - calendar_api_key (str): API key for Cal.com authentication
            - event_id (int, optional): The identifier of the event type being booked, it is eventtypes id
            - slotStart (str, optional): The start time of the slot to be booked
        to_calendar_availability_agent (callable, optional): Function to check availability. Defaults to None.
        to_calendar_booking_agent (callable, optional): Function to book appointment. Defaults to None.
    """
    print("Transferring to calendar agent with api key: ", context_variables["calendar_api_key"])
    print("\n\n Calendar agent context variables: ", context_variables)
    return calendar_agent



calendar_agent = Agent(
    name="Calendar Agent",
    instructions=CALENDAR_AGENT_INSTRUCTIONS,
    parallel_tool_calls=True,
)
calendar_agent.functions = [to_calendar_availability_agent, to_calendar_booking_agent]


print("\n\n Calendar agent: ", calendar_agent.name)
# Interface agent
#     -> Calendar Agent
#         -> Get Calendar Detail such as EventID 
#             -> Use API key to get all events for that API key and ask for type of slot like 15 min, 30 min, etc
#         -> Check Availability (EventID, StartTime is passed and then it is used to get slots)
#             -> Return top slots in set of 3
#         -> Reserve Slot (To avoid Race Condition, utilize EventId, StartTime and EndTime)
#             -> Now Slot is reserved for the person and at the same time as soon as slot is reserved book the slot
#         -> Book Appointment (using EventId, StartTime)
#             -> Return "success" or "failure"



# AGENTS: 
#     -> Interface Agent 
#         -> Calendar Agent 
#             -> Event Details Agent
#                 -> get_events_from_calendar()
#             -> Availability Agent 
#                 -> check_all_availabile_slots()
#             -> Reserve Slot Agent 
#                 -> reserve_slot_for_startTime()
#             -> Book Appointment Agent 
#                 -> book_appointment_for_startTime()
#         -> Human Agent 
#             -> transfer_to_human()