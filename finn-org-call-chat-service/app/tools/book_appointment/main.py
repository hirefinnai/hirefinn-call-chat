# All the appointment related tools will be implemented here
from swarm import Agent


def book_appointment(appointment_details):

    return "Appointment booked"



def transfer_to_book_appointment():
    print("Transferring to book appointment")
    return book_appointment_agent



book_appointment_agent = Agent(
    name = "Book Appointment Agent",
    instructions = "You have to book the appointment for the user",
    functions = [book_appointment]
)


