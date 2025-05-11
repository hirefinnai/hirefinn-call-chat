# All the event details related tools will be implemented here
from swarm import Agent
import requests


def get_eventId_from_calendar(calendar_api_key):
    '''
    Get all the event types from the calendar.
    Args:
        calendar_api_key (str): API key for Cal.com authentication
    '''
    print("\n\n Getting eventId from calendar with api key: ", calendar_api_key)
    
    url = "https://api.cal.com/v1/event-types"
    headers = {
        "accept": "application/json"
    }
    params = {
        "apiKey": calendar_api_key
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        event_types = response.json()
        print("\n\n Event types: ", event_types)
        if event_types and len(event_types["event_types"]) > 0:
            # Return all event details instead of just first ID
            return {
                "event_types": [{
                    "id": event["id"],
                    "title": event["title"], 
                    "length": event["length"],
                    "hidden": event["hidden"]
                } for event in event_types["event_types"] if not event["hidden"]]
            }
    return None

def get_events_from_calendar(context_variables):
    '''
    Use this function to get all the events from the calendar.
    Args:
        context_variables (dict): A dictionary containing booking context information.
            - calendar_api_key (str): API key for Cal.com authentication
            - event_id (int, optional): The identifier of the event type being booked, it is eventtypes id  
            - slotStart (str, optional): The start time of the slot to be booked
    '''
    print("\n\n Getting events from calendar with api key: ", context_variables["calendar_api_key"])

    # Get all events from calendar
    event_details = get_eventId_from_calendar(context_variables["calendar_api_key"])
    if event_details and len(event_details["event_types"]) > 0:
        # Store first event ID in context but return full details
        context_variables["event_id"] = event_details["event_types"][0]["id"]
        print("\n\n Event id: ", context_variables["event_id"])
        return event_details
    return None