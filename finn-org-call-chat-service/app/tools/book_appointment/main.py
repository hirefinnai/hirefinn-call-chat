# All the reserve slot related tools will be implemented here
import requests

def book_appointment_for_startTime(context_variables, name:str, email:str):
    '''
    Use this function to book an appointment in Cal.com using the provided context variables.

    Args:
        context_variables (dict): A dictionary containing booking context information.
            - calendar_api_key (str): API key for Cal.com
            - event_id (int, optional): The Cal.com event type ID
            - slotStart (str, optional): ISO formatted start time for the appointment
            - name (str, optional): Name of the person booking. Defaults to "Default Name2"
            - email (str, optional): Email of the person booking. Defaults to "default@email.com"
    '''
    print("\n\n Booking appointment with event id:", context_variables["event_id"])
    print("Booking appointment with slot start:", context_variables["slotStart"])

    url = "https://api.cal.com/v1/bookings"
    params = {
        "apiKey": context_variables["calendar_api_key"]
    }
    payload = {
        "eventTypeId": context_variables["event_id"],
        "start": context_variables["slotStart"],
        "responses": {
            "name": context_variables.get("name", "Default Name2"),
            "email": context_variables.get("email", "default@email.com"),
            "location": {
                "value": "",
                "optionValue": ""
            }
        },
        "metadata": {},
        "timeZone": "Asia/Calcutta",
        "language": "en",
        "title": "Meeting With Kevin",
        "description": "Meeting scheduled via chat",
        "status": "PENDING"
    }

    try:
        response = requests.post(url, params=params, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            print("Booking response:", response_json)
            return "Appointment booked successfully"
        else:
            print("Error booking appointment:", response.status_code, response.text)
            return f"Failed to book appointment: {response.status_code} {response.text}"
    except requests.exceptions.RequestException as e:
        print("Error booking appointment:", str(e))
        return f"Failed to book appointment: {str(e)}"