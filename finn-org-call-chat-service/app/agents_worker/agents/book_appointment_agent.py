from tools.book_appointment.main import book_appointment_for_startTime
from swarm import Agent
from agents_worker.instructions import BOOK_APPOINTMENT_AGENT_INSTRUCTIONS

def to_book_appointment_agent(context_variables, book_appointment_for_startTime):
    """
    This agent is strictly called after the slot is reserved.
    Transfers control to the Book Appointment Agent to finalize the booking process.
    
    This function should be called strictly after a slot has been successfully reserved by the Reserve Slot Agent.
    It handles the final confirmation and creation of the appointment in the calendar system.
    
    The Book Appointment Agent is responsible for:
    - Converting temporary slot reservations into permanent bookings
    - Creating the final calendar event with all necessary details
    - Handling any required notifications or confirmations
    - Cleaning up temporary reservations upon successful booking
    
    Args:
        context_variables (dict): A dictionary containing booking context information including:
            - slotStart (str): The start time of the slot to be booked
            - event_id (str): The identifier of the event type being booked
            - attendee_details (dict): Information about the person booking the appointment
            - Other relevant booking details passed from previous agents
        book_appointment_for_startTime (function): A function that books an appointment for a given start time. You must call this function.
    Returns:
        Agent: Returns the book_appointment_agent instance that handles the final booking process
               using the book_appointment_for_startTime function.
    Always call this function book_appointment_for_startTime().
    Note:
        - This agent must be called after successful slot reservation
        - The agent uses book_appointment_for_startTime to create the final calendar appointment
        - If booking fails, appropriate error handling should be implemented
        - The booking process is considered complete only after this agent successfully executes
        - This is the final step in the booking workflow and should trigger any necessary notifications
    Always call this function book_appointment_for_startTime().
    """
    print("\n\n Context variables: ", context_variables)
    print("Transferring to book appointment for start time: ", context_variables["slotStart"])
    return book_appointment_agent



book_appointment_agent = Agent(
    name = "Book Appointment Agent",
    instructions = BOOK_APPOINTMENT_AGENT_INSTRUCTIONS,
    parallel_tool_calls=True,
)

book_appointment_agent.functions = [book_appointment_for_startTime]

print("\n\n Book appointment agent: ", book_appointment_agent.name)