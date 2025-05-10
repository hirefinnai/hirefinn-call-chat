# All the reserve slot related tools will be implemented here
import requests

def book_appointment_for_startTime(context_variables):
    '''
    Books an appointment in Cal.com using the provided context variables.
    
    This function should be called after a slot has been reserved and the user has confirmed
    they want to book the appointment. It makes a POST request to Cal.com's booking API
    to create a new appointment.

    Args:
        context_variables (dict): A dictionary containing:
            - event_id (str): The Cal.com event type ID
            - slotStart (str): ISO formatted start time for the appointment
            - calendar_api_key (str): API key for Cal.com
            - name (str, optional): Name of the person booking. Defaults to "Default Name"
            - email (str, optional): Email of the person booking. Defaults to "default@email.com"

    Returns:
        str: A success or failure message indicating the booking status
            - "Appointment booked successfully" if booking succeeds
            - Error message with details if booking fails

    Raises:
        No explicit raises, but handles all exceptions and returns error messages as strings
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