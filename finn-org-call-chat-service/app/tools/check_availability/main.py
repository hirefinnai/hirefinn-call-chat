# All the calendar details will be implemented here
import requests
import time
from datetime import datetime

def slots_from_calendar(calendar_api_key:str):
    '''
    Get all the slots from the calendar for the given event id.
    Args:
        calendar_api_key (str): API key for Cal.com authentication
    '''
    try:
        # Get event_id from agent instance
        event_id = None
        from agents_worker.main import HireFinnAgent
        agent_instance = None
        
        import inspect
        frame = inspect.currentframe()
        while frame:
            if 'self' in frame.f_locals and isinstance(frame.f_locals['self'], HireFinnAgent):
                agent_instance = frame.f_locals['self']
                if agent_instance.event_id:
                    event_id = agent_instance.event_id
                break
            frame = frame.f_back
                
        if not event_id:
            print("Error: event_id missing from agent instance")
            return None

        print("Getting all slots from calendar with event id: ", event_id)
        
        # Set up API request parameters
        start_time = time.time()
        start_time = start_time + (2 * 24 * 60 * 60)  # Get slots for next 7 days in seconds
        end_time = start_time + (2 * 24 * 60 * 60)  # Get slots for next 7 days in seconds
        url = f"https://api.cal.com/v2/slots"
        headers = {
            "Authorization": f"Bearer {calendar_api_key}", 
            "cal-api-version": "2024-09-04"
        }
        params = {
            "start": datetime.fromtimestamp(start_time).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "end": datetime.fromtimestamp(end_time).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "eventTypeId": event_id
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
            
            if agent_instance:
                agent_instance.slotStart = first_slot["start"]
                
            print("\n\n Slot start: ", first_slot["start"])
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
    
    
def check_all_availabile_slots(calendar_api_key:str):
    '''
    Use this function to check all the available slots for the given event id.
    Args:
        calendar_api_key (str): API key for Cal.com authentication
    '''
    try:
        # Get event_id from agent instance
        event_id = None
        from agents_worker.main import HireFinnAgent
        
        import inspect
        frame = inspect.currentframe()
        while frame:
            if 'self' in frame.f_locals and isinstance(frame.f_locals['self'], HireFinnAgent):
                agent_instance = frame.f_locals['self']
                if agent_instance.event_id:
                    event_id = agent_instance.event_id
                break
            frame = frame.f_back
        
        print("\n\n Checking all available slots with event id: ", event_id)
        calendar_details = slots_from_calendar(calendar_api_key)
        print("Checking all available slots with event id: ", event_id)
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