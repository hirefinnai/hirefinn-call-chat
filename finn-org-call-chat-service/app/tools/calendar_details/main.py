# All the calendar details will be implemented here
from swarm import Agent


def get_calendar_details():
    calendar_details = """
        # May 2025 Tech Calendar

        | Date       | Time        | Status      | Details                                     |
        |------------|-------------|-------------|---------------------------------------------|
        | May 1      | 09:00-10:30 | Available   |                                             |
        | May 1      | 13:00-14:00 | *BOOKED*  | Kubernetes cluster upgrade                  |
        | May 1      | 15:00-16:30 | Available   |                                             |
        | May 2      | 10:00-11:00 | Available   |                                             |
        | May 2      | 14:00-15:30 | *BOOKED*  | Code review session for API refactoring     |
        | May 5      | 09:30-11:00 | Available   |                                             |
        | May 5      | 13:00-15:00 | *BOOKED*  | React component library workshop            |
        | May 6      | 11:00-12:00 | Available   |                                             |
        | May 6      | 14:00-16:00 | Available   |                                             |
        | May 7      | 09:00-10:00 | *BOOKED*  | Docker optimization call                    |
        | May 7      | 13:30-14:30 | Available   |                                             |
        | May 8      | 10:00-12:00 | Available   |                                             |
        | May 8      | 15:00-16:00 | *BOOKED*  | GraphQL schema design meeting               |
        | May 9      | 09:00-10:30 | Available   |                                             |
        | May 9      | 14:00-15:00 | *BOOKED*  | AWS infrastructure security audit           |
        | May 12     | 11:00-12:30 | Available   |                                             |
        | May 12     | 15:30-17:00 | *BOOKED*  | PostgreSQL performance tuning session       |
        | May 13     | 09:00-11:00 | Available   |                                             |
        | May 13     | 13:00-14:30 | *BOOKED*  | Machine learning model review               |
        | May 14     | 10:00-12:00 | Available   |                                             |
        | May 14     | 14:00-15:00 | Available   |                                             |
        | May 15     | 09:30-11:00 | *BOOKED*  | CI/CD pipeline troubleshooting              |
        | May 15     | 13:00-14:30 | Available   |                                             |
        | May 16     | 11:00-12:00 | *BOOKED*  | Microservice architecture planning          |
        | May 16     | 15:00-16:30 | Available   |                                             |
    """
    return calendar_details



def transfer_to_calendar_details():
    print("Transferring to calendar details")
    return calendar_details_agent



calendar_details_agent = Agent(
    name = "Calendar Details Agent",
    instructions = "You have to provide the calendar details to check availability",
    functions = [get_calendar_details]
)





