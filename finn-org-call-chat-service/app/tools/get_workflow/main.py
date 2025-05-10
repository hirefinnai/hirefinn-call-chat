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
                "name": "Get Calendar Details",
                "content": "1. Call function get_events_from_calendar to retrieve event details and event ID\n2. Use event ID to get available event types and details",
                "contentType": "Prompt"
            },
            {
                "id": "Task3",
                "name": "Check Availability",
                "content": "1. Ask user when they would like to schedule.\n2. Call function check_all_availabile_slots to check available time slots",
                "contentType": "Prompt"
            },
            {
                "id": "Task4",
                "name": "Reserve Slot",
                "content": "Call function reserve_slot_for_startTime to reserve the selected time slot",
                "contentType": "Prompt"
            },
            {
                "id": "Task5",
                "name": "Book Appointment",
                "content": "Call function book_appointment_for_startTime to finalize the booking",
                "contentType": "Prompt"
            },
            {
                "id": "Task6",
                "name": "Winding Up",
                "content": "say 'Thank you for your time. Your appointment has been booked. If you have any questions, feel free to reach out. Have a great day! Goodbye!'",
                "contentType": "Static"
            }
        ],
        "edges": [
            {
                "from": "Task1",
                "to": "Task2",
                "condition": "user confirms identity"
            },
            {
                "from": "Task2",
                "to": "Task3", 
                "condition": "calendar details and event types retrieved successfully"
            },
            {
                "from": "Task3",
                "to": "Task4",
                "condition": "suitable slot found"
            },
            {
                "from": "Task4",
                "to": "Task5",
                "condition": "slot reserved successfully"
            },
            {
                "from": "Task5",
                "to": "Task6",
                "condition": "appointment booked successfully"
            }
        ]
    }

    return workflow

