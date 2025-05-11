from tools.reserve_slot.main import reserve_slot_for_startTime
from agents_worker.agents.book_appointment_agent import to_book_appointment_agent
from swarm import Agent
from agents_worker.instructions import RESERVE_SLOT_AGENT_INSTRUCTIONS

def to_reserve_slot_agent(context_variables, reserve_slot_for_startTime=None, to_book_appointment_agent=None):
    """
    Always call this when user asks to reserve a slot or book an appointment.
    Transfers control to the Reserve Slot Agent to handle slot reservation in the booking flow.
    Args:
        context_variables (dict): A dictionary containing booking context information including:
            - event_id (int, optional): The identifier of the event type being booked, it is eventtypes id
            - calendar_api_key (str): API key for Cal.com authentication
            - slotStart (str, optional): The start time of the slot to be booked
            - attendee_details (dict): Information about the person booking the appointment
        reserve_slot_for_startTime (callable, optional): Function to reserve slot. Defaults to None.
        to_book_appointment_agent (callable, optional): Function to book appointment. Defaults to None.
    """
    print("Transferring to reserve slot: ", context_variables["slotStart"])
    print("Transferring to check availability: ", context_variables["event_id"])
    return reserve_slot_agent



reserve_slot_agent = Agent(
    name = "Reserve Slot Agent",
    instructions = RESERVE_SLOT_AGENT_INSTRUCTIONS,
    parallel_tool_calls=True,
)
reserve_slot_agent.functions = [reserve_slot_for_startTime, to_book_appointment_agent]


print("\n\nReserve slot agent: ", reserve_slot_agent.name)