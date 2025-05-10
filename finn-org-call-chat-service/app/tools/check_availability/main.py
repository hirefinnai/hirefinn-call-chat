
# All the calendar details will be implemented here
import requests
import time
from datetime import datetime

def slots_from_calendar(context_variables):
    '''
    Retrieves available time slots from Cal.com calendar for a specific event type.
    
    This function should be called when you need to fetch available slots for the next 2 days
    for a specific event type. It uses Cal.com's v2 API to get slot availability.

    Args:
        context_variables (dict): A dictionary containing:
            - event_id (str): The Cal.com event type ID to check slots for
            - calendar_api_key (str): API key for Cal.com authentication

    Returns:
        dict: A dictionary containing the first available slot with format:
            {
                "data": {
                    "date": [{
                        "start": "ISO timestamp",
                        ...other slot details
                    }]
                },
                "status": "success"
            }
        None: If no slots are available or if the API call fails

    Note:
        Currently only returns the first available slot. May need modification to return
        multiple slots based on requirements.
    '''
    try:
        if "event_id" not in context_variables:
            print("Error: event_id missing from context variables")
            return None
            
        if "calendar_api_key" not in context_variables:
            print("Error: calendar_api_key missing from context variables") 
            return None

        print("Getting all slots from calendar with event id: ", context_variables["event_id"])
        
        # Set up API request parameters
        start_time = time.time()
        start_time = start_time + (2 * 24 * 60 * 60)  # Get slots for next 7 days in seconds
        end_time = start_time + (2 * 24 * 60 * 60)  # Get slots for next 7 days in seconds
        url = f"https://api.cal.com/v2/slots"
        headers = {
            "Authorization": f"Bearer {context_variables['calendar_api_key']}", 
            "cal-api-version": "2024-09-04"
        }
        params = {
            "start": datetime.fromtimestamp(start_time).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "end": datetime.fromtimestamp(end_time).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "eventTypeId": context_variables["event_id"]
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error: API request failed with status code {response.status_code}")
            return None
            
        response_json = response.json()
        print("\n\n Slots: ", response_json)

        if not response_json:
            print("Error: Empty response from API")
            return None

        if response_json.get("status") != "success":
            print(f"Error: API returned non-success status: {response_json.get('status')}")
            return None

        if not response_json.get("data"):
            print("No available slots found")
            return None

        # Get first date and first time slot
        try:
            first_date = next(iter(response_json["data"]))
            first_slot = response_json["data"][first_date][0]
            context_variables["slotStart"] = first_slot["start"]
            print("\n\n Slot start: ", context_variables["slotStart"])
            return {"data": {first_date: [first_slot]}, "status": "success"}
        except (StopIteration, KeyError, IndexError) as e:
            print(f"Error processing slot data: {str(e)}")
            return None
            
    except requests.RequestException as e:
        print(f"Network error occurred: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        return None
    
    
def check_all_availabile_slots(context_variables):
    '''
    Wrapper function to check all available slots for a given event type.
    
    This function should be called when you need to present available time slots to a user
    for booking. It internally calls slots_from_calendar to get the slot data.

    Args:
        context_variables (dict): A dictionary containing:
            - event_id (str): The Cal.com event type ID to check slots for
            - calendar_api_key (str): API key for Cal.com authentication

    Returns:
        dict: Calendar details containing available slots in the same format as slots_from_calendar
        None: If no slots are found or if there's an error
    '''
    try:
        print("\n\n Checking all available slots with event id: ", context_variables["event_id"])
        calendar_details = slots_from_calendar(context_variables)
        print("Checking all available slots with event id: ", context_variables["event_id"])
        print("\n\n Calendar details: ", calendar_details)
        return calendar_details
    except Exception as e:
        print(f"Error checking available slots: {str(e)}")
        return None


# # Call the function with required context variables
# context = {
#     "event_id": "2367134",
#     "calendar_api_key": "cal_live_d6663bd0bc8047c4d83501365dbcc266" 
# }
# check_all_availabile_slots(context)