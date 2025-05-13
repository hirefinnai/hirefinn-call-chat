# All the reserve slot related tools will be implemented here
from swarm import Agent
import requests

def reserve_slot_for_startTime(context_variables, calendar_api_key:str):
    '''
    Use this function to reserve a slot for the given event id.
    Args:
        context_variables (dict): A dictionary containing booking context information.
            - calendar_api_key (str): API key for Cal.com authentication
            - event_id (int): The Cal.com event type ID
            - slotStart (str): ISO formatted start time for the slot to reserve
    '''
    print("Reserving slot with event id:", context_variables["event_id"])
    
    url = "https://api.cal.com/v2/slots/reservations"
    headers = {
        "Authorization": f"Bearer {calendar_api_key}",
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