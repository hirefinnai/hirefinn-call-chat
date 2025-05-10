from tools.reserve_slot.main import reserve_slot_for_startTime
from agents_worker.agents.book_appointment_agent import to_book_appointment_agent
from swarm import Agent
from agents_worker.instructions import RESERVE_SLOT_AGENT_INSTRUCTIONS

def to_reserve_slot_agent(context_variables, reserve_slot_for_startTime):
    """
    Always call this when user asks to book an appointment.
    Transfers control to the Reserve Slot Agent to handle slot reservation in the booking flow.
    
    This function should be called strictly after availability has been confirmed and before final booking.
    It acts as a critical synchronization point to prevent double-bookings by temporarily reserving the slot.
    
    The Reserve Slot Agent is responsible for:
    - Creating a temporary hold on the selected time slot
    - Ensuring atomic booking operations to prevent race conditions
    - Validating that the slot is still available before reserving
    - Managing the transition between availability check and final booking
    - Always call this function after availability has been confirmed and before final booking.
    Args:
        context_variables (dict): A dictionary containing necessary context information including:
            - slotStart (str): The start time of the slot to be reserved
            - event_id (str): The identifier of the event type being reserved
            - attendee_details (dict): Information about the person booking the appointment
            - Other relevant booking details passed from previous agents    
        reserve_slot_for_startTime (function): A function that reserves a slot for a given start time. You must call this function.
    Returns:
        Agent: Returns the reserve_slot_agent instance that handles the slot reservation process
               using the reserve_slot_for_startTime function.
    
    Note:
        - This agent must be called before the Book Appointment Agent to maintain booking integrity
        - The agent uses reserve_slot_for_startTime to create a temporary hold on the selected time slot
        - If reservation fails, the booking process should be aborted
        - Reservations typically have a short time-to-live to prevent indefinite holds
        - This is a critical step in preventing double-bookings in high-concurrency scenarios
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