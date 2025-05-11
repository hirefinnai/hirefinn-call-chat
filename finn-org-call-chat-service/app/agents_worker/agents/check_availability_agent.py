from tools.check_availability.main import check_all_availabile_slots
from agents_worker.agents.reserve_slot_agent import to_reserve_slot_agent
from agents_worker.agents.book_appointment_agent import to_book_appointment_agent
from swarm import Agent
from agents_worker.instructions import CHECK_AVAILABILITY_AGENT_INSTRUCTIONS

def to_check_availability_agent(context_variables, check_all_availabile_slots=None, to_reserve_slot_agent=None, to_book_appointment_agent=None):
    """
    Transfer control to the Check Availability Agent to get the available slots for the event.
    Args:
        context_variables (dict): A dictionary containing booking context information including:
            - event_id (int, optional): The identifier of the event type being booked, it is eventtypes id
            - calendar_api_key (str): API key for Cal.com authentication
            - slotStart (str, optional): The start time of the slot to be booked
            - slotEnd (str, optional): The end time of the slot to be booked
        check_all_availabile_slots (callable, optional): Function to check available slots. Defaults to None.
        to_reserve_slot_agent (callable, optional): Function to reserve slot. Defaults to None.
        to_book_appointment_agent (callable, optional): Function to book appointment. Defaults to None.
    """
    print("Transferring to check availability with event id: ", context_variables["event_id"])
    return check_availability_agent


check_availability_agent = Agent(
    name = "Check Availability Agent",
    instructions = CHECK_AVAILABILITY_AGENT_INSTRUCTIONS,
    parallel_tool_calls=True,
)

check_availability_agent.functions = [check_all_availabile_slots, to_reserve_slot_agent, to_book_appointment_agent]

print("\n\n Check availability agent: ", check_availability_agent.name)