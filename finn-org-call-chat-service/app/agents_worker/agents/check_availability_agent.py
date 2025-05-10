from tools.check_availability.main import check_all_availabile_slots
from agents_worker.agents.reserve_slot_agent import to_reserve_slot_agent
from agents_worker.agents.book_appointment_agent import to_book_appointment_agent
from swarm import Agent
from agents_worker.instructions import CHECK_AVAILABILITY_AGENT_INSTRUCTIONS

def to_check_availability_agent(context_variables, check_all_availabile_slots):
    """
    Transfers control to the Check Availability Agent which determines available time slots for booking.
    This agent is called after event details have been retrieved and before slot reservation.

    The Check Availability Agent is responsible for:
    - Querying available time slots for a specific event type
    - Filtering slots based on business rules and constraints
    - Returning a curated list of available booking times (typically in sets of 3)

    Args:
        context_variables (dict): A dictionary containing necessary context information including:
            - event_id (str): Identifier for the event type to check availability for
            - calendar_api_key (str): API key for Cal.com authentication
        check_all_availabile_slots (function): A function that checks all available slots for a given event type. You must call this function.
    Returns:
        Agent: Returns the check_availability_agent instance that handles slot availability checking
              using the check_all_availabile_slots function

    Note:
        - This agent must be called after event details are retrieved
        - The agent ensures slots returned are actually available for booking
        - Successful execution is required before proceeding to slot reservation
        - Returns multiple slot options to provide flexibility in booking
    """
    print("Transferring to check availability with event id: ", context_variables["event_id"])
    return check_availability_agent



check_availability_agent  =  Agent(
    name = "Check Availability Agent",
    instructions = CHECK_AVAILABILITY_AGENT_INSTRUCTIONS,
    parallel_tool_calls=True,
)
check_availability_agent.functions = [check_all_availabile_slots, to_reserve_slot_agent, to_book_appointment_agent]

print("\n\n Check availability agent: ", check_availability_agent.name)