from tools.book_appointment.main import book_appointment_for_startTime
from swarm import Agent
from agents_worker.instructions import BOOK_APPOINTMENT_AGENT_INSTRUCTIONS

def to_book_appointment_agent(context_variables: dict, book_appointment_for_startTime=None):
    """
    Transfer control to the Book Appointment Agent to book the appointment.
    Args:
        - context_variables (dict): A dictionary containing booking context information including:
            - calendar_api_key (str): API key for Cal.com authentication
            - event_id (int, optional): The identifier of the event type being booked, it is eventtypes id
            - slotStart (str, optional): The start time of the slot to be booked
            - attendee_details (dict): Information about the person booking the appointment
        book_appointment_for_startTime (callable, optional): Function to book appointment. Defaults to None.
    """
    print("\n\n Book appointment agent context variables: ", context_variables)
    return book_appointment_agent



book_appointment_agent = Agent(
    name = "Book Appointment Agent",
    instructions = "Use the book_appointment_for_startTime function to book the appointment.",
    parallel_tool_calls=True,
)

book_appointment_agent.functions = [book_appointment_for_startTime]

print("\n\n Book appointment agent: ", book_appointment_agent.name)