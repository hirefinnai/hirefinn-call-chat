# All the event details related tools will be implemented here
from swarm import Agent
import requests


def get_eventId_from_calendar(calendar_api_key):
    '''
    Retrieves all available event types from Cal.com calendar.
    
    This function should be called at the start of the booking flow to get a list of
    available event types that can be booked. It filters out hidden events.

    Args:
        calendar_api_key (str): API key for Cal.com authentication

    Returns:
        dict: A dictionary containing event type details with format:
            {
                "event_types": [
                    {
                        "id": str,
                        "title": str,
                        "length": int,
                        "hidden": bool
                    },
                    ...
                ]
            }
        None: If no event types are found or if the API call fails

    Note:
        Only returns non-hidden events to ensure only bookable events are displayed
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
    Wrapper function to get all available events and store the first event ID in context.
    
    This function should be called when you need to both retrieve available events and
    automatically select the first event for booking. It internally calls get_eventId_from_calendar.

    Args:
        context_variables (dict): A dictionary containing:
            - calendar_api_key (str): API key for Cal.com authentication

    Returns:
        dict: Event details in the same format as get_eventId_from_calendar
        None: If no events are found or if there's an error

    Side Effects:
        Sets context_variables["event_id"] to the ID of the first available event
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