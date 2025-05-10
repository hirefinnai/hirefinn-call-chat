from agents_worker.agents.event_details_agent import to_event_details_agent
from agents_worker.agents.check_availability_agent import to_check_availability_agent
from agents_worker.agents.reserve_slot_agent import to_reserve_slot_agent
from agents_worker.agents.book_appointment_agent import to_book_appointment_agent
from swarm import Agent
from agents_worker.instructions import CALENDAR_AGENT_INSTRUCTIONS

def to_calendar_agent(context_variables):
    """
    Main entry point for calendar-related operations. This function transfers control to the Calendar Agent
    which orchestrates the entire appointment booking flow.

    The Calendar Agent serves as the primary coordinator for the following sequence of operations:
    1. Retrieving event details and available slot types (via Event Details Agent)
    2. Checking slot availability (via Check Availability Agent)
    3. Reserving slots to prevent double bookings (via Reserve Slot Agent)
    4. Finalizing appointment bookings (via Book Appointment Agent)
    Always call the reserve_slot_agent first and then call the book_appointment_agent.
    When user asks to book an appointment, immediately execute the following sequence:
    1. to_event_details_agent()
    2. to_check_availability_agent()
    3. to_reserve_slot_agent()
    4. to_book_appointment_agent()
    Always execute the above sequence in the exact order.
    When user ask to book appointment always execute the above sequence.
    Do not skip any steps.
    Do not change the order of the sequence.
    Do not add any other steps in the sequence.
    Do not remove any steps from the sequence.
    Do not change the sequence of the steps.
    Do not add any other steps in the sequence.
    Do not remove any steps from the sequence.
    Strictly follow the sequence.
    Do not skip any steps.
    Args:
        context_variables (dict): A dictionary containing necessary context information including:
            - calendar_api_key (str): API key for calendar access
            - Additional context variables may be required for specific sub-agents
        to_event_details_agent (function): A function that transfers control to the Event Details Agent.
        to_check_availability_agent (function): A function that transfers control to the Check Availability Agent.
        to_reserve_slot_agent (function): A function that transfers control to the Reserve Slot Agent.
        to_book_appointment_agent (function): A function that transfers control to the Book Appointment Agent.
    Returns:
        Agent: Returns the calendar_agent instance that orchestrates the entire booking workflow

    Note:
        - This is the main coordinator agent that manages the entire booking flow
        - All calendar operations are performed through this agent's sub-agents
        - The agent maintains the state and context throughout the booking process
    """
    print("Transferring to calendar agent with api key: ", context_variables["calendar_api_key"])
    print("\n\n Context variables: ", context_variables)
    return calendar_agent



calendar_agent = Agent(
    name="Calendar Agent",
    instructions=CALENDAR_AGENT_INSTRUCTIONS,
    parallel_tool_calls=True,
)
calendar_agent.functions = [to_event_details_agent, to_check_availability_agent, to_reserve_slot_agent, to_book_appointment_agent]


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