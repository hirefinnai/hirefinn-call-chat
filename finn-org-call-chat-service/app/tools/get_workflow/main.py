from swarm import Agent

def get_workflow():
    workflow = {
        "nodes": [
            {
                "id": "Task1",
            "name": "Greetings",
            "content": "say 'Hello, this is John, An AI representative calling from Omega HMS Healthcare organization. I'm reaching out to help you access your health service portal, May I speak with Akarsh, please?'",
            "contentType": "Static"
        },
        {
            "id": "Task2",
            "name": "Check Calendar availability",
            "content": "1. Ask user when they are available for the tour.\n2. Call function check_calendar_availability to check for availability in the user provided time range.",
            "contentType": "Prompt"
        },
        {
            "id": "Task3",
            "name": "Winding Up",
            "content": "say 'Thank you for your time. If you have any further questions, feel free to reach out to us. Have a great day! Goodbye!'",
            "contentType": "Static"
        }
    ],
    "edges": [
        {
            "from": "Task1",
            "to": "Task2",
            "condition": "user said yes or shows interests"
        },
        {
            "from": "Task1",
            "to": "Task3",
            "condition": "user is a bit hesitant or has no interest"
        },
        {
            "from": "Task2",
            "to": "Task3",
                "condition": "user is a bit hesitant or has no interest"
            }
        ]
    }

    return workflow


def transfer_to_get_workflow():
    print("Transferring to get workflow")
    return get_workflow_agent



get_workflow_agent = Agent(
    name = "Get Workflow Agent",
    instructions = "You have to get the workflow for the user",
    functions = [get_workflow]
)


