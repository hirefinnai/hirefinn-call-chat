# All the availability related tools will be implemented here
from swarm import Agent


def transfer_to_check_availability():
    print("Transferring to check availability")
    return check_availability_agent




def check_availability():
    print("Checking availability")
    return "Date is available"


check_availability_agent  =  Agent(
    name = "Check Availability Agent",
    instructions = "You have to check the availability of the date provided by the user in the calendar details, and return the availability status",
    functions = [check_availability]
)
