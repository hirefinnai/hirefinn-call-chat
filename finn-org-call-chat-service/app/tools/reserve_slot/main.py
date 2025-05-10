# All the reserve slot related tools will be implemented here
from swarm import Agent
import requests

def reserve_slot_for_startTime(context_variables):
    '''
    Temporarily reserves a time slot in Cal.com to prevent double booking.
    
    This function should be called after a user has selected a specific time slot but before
    finalizing the booking. It creates a temporary hold on the slot to prevent other users
    from booking it while the current user completes their booking process.

    Args:
        context_variables (dict): A dictionary containing:
            - event_id (str): The Cal.com event type ID
            - slotStart (str): ISO formatted start time for the slot to reserve
            - calendar_api_key (str): API key for Cal.com authentication

    Returns:
        str: A success or failure message indicating the reservation status
            - "Slot reserved successfully" if reservation succeeds
            - Error message with details if reservation fails

    Note:
        The reservation is temporary and will expire after a short period if not confirmed
        with a booking. This is handled by Cal.com's backend.
    '''
    print("Reserving slot with event id:", context_variables["event_id"])
    
    url = "https://api.cal.com/v2/slots/reservations"
    headers = {
        "Authorization": f"Bearer {context_variables['calendar_api_key']}",
        "Content-Type": "application/json",
        "cal-api-version": "2024-09-04"
    }
    payload = {
        "eventTypeId": context_variables["event_id"],
        "slotStart": context_variables["slotStart"]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            print("Slot reservation response:", response_json)
            return "Slot reserved successfully"
        else:
            print("Error reserving slot:", response.status_code, response.text)
            return f"Failed to reserve slot: {response.status_code} {response.text}"
    except requests.exceptions.RequestException as e:
        print("Error reserving slot:", str(e))
        return f"Failed to reserve slot: {str(e)}"