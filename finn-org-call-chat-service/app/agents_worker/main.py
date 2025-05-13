# All the calendar details will be implemented here
import time
from datetime import datetime
from swarm import Swarm
from openai import OpenAI
from rag_content.main import RagContent
import json
from swarm import Agent
import os
import requests


# Initialize OpenAI client
openai_client = OpenAI(api_key="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")

# Initialize Swarm client with OpenAI client
client = Swarm(openai_client)

class HireFinnAgent:
    def __init__(self):
        self.rag_content="cal_live_349f]a2e7b5e16684b3f89915cc17f356"
        self.calendar_api_key="cal_live_349fa2e7b5e16684b3f89915cc17f356"
        self.event_id=2444587,
        self.slotStart="2025-06-15T16:00:00.000Z",
        self.name="John Doe"
        self.email="john.doe@example.com"
        self.agent = Agent(
            name="Finn Interface Agent",
            instructions="""You must always answer in 1-2 sentences. You are a helpful assistant that can help with calendar bookings. You have to utilize the tools provided to you to help the user with their calendar bookings. 
            You can check event details, check availability of slots, reserve slots and book appointments.
            You must first get event details, then check availability of slots, then reserve slots and then book appointments.
            You have to follow the following steps in order:
            1. Get event details using get_events_from_calendar tool(calendar_api_key": self.calendar_api_key, "event_id": self.event_id, "slotStart": self.slotStart)
            2. Check availability of slots using check_all_availabile_slots tool(calendar_api_key": self.calendar_api_key, "event_id": self.event_id, "slotStart": self.slotStart)
            3. Reserve slots using reserve_slot_for_startTime tool(calendar_api_key": self.calendar_api_key, "event_id": self.event_id, "slotStart": self.slotStart)
            4. Book appointments using book_appointment_for_startTime tool(calendar_api_key": self.calendar_api_key, "event_id": self.event_id, "slotStart": self.slotStart)
            Do not skip any steps.
            You must always pass the calendar_api_key to the tools as argument, in context_variables.
            If the user asks you to book an appointment, you must first get event details, then check availability of slots, then reserve slots and then book appointments.
            If user just wants to check availability of slots, you must use event details and check availability of slots.
            Only reserve slots if user wants to book an appointment.

            You must always use the tools calls if the user query is related to calendar.
            You already have the calendar_api_key, event_id, slotStart, name and email in context.

            # Strict Policy:
            ## You must always return complete response, never return response like "Please wait while I check the availability of slots" or "Please wait while I reserve the slot" or "Please hold on" or "I am checking the availability of slots" or "I am reserving the slot" or "I am booking the appointment".
            ## You must always return the complete response in one go, never return partial response.
            """,
            parallel_tool_calls=True,
            )

    async def extract_rag_content(self, org_id, agent_id, user_input):
        rag_worker = RagContent()
        self.rag_content = await rag_worker.get_rag_content(org_id=org_id , agent_id=agent_id, query=user_input)

        print("RAG content: ", self.rag_content)
        return self.rag_content

    async def get_assistant_response(self,  messages, calendar_api_key, org_id, agent_id, user_input, use_case, language, indentity_text, guardrails, response_guidelines, welcome_message, call_workflow, finn_name):
        print("Calendar API key: ", calendar_api_key)
        
        # Get response from agent
        assistant_response = client.run(
            agent=self.agent,
            messages=messages,
            debug=True,
        )

        response_content = assistant_response.messages[-1]["content"]
        print("Response content: ", response_content)
        try:
            # Try to parse the response as JSON
            return response_content
        except:
            # If parsing fails, return a default format
            return "Something went wrong. Please try again later."

    # All the reserve slot related tools will be implemented here
    def book_appointment_for_startTime(self, calendar_api_key:str, event_id:str, slotStart:str, name:str, email:str):
        '''
        Use this function to book an appointment in Cal.com using the provided context variables.

        Args:
            context_variables (dict): A dictionary containing booking context information.
                - calendar_api_key (str): API key for Cal.com
                - event_id (int): The Cal.com event type ID
                - slotStart (str): ISO formatted start time for the appointment
                - name (str): Name of the person booking. Defaults to "Default Name2"
                - email (str): Email of the person booking. Defaults to "default@email.com"
        '''
        print("\n\n Booking appointment with event id:", event_id)
        print("Booking appointment with slot start:", slotStart)

        url = "https://api.cal.com/v1/bookings"
        params = {
            "apiKey": calendar_api_key
        }
        payload = {
            "eventTypeId": event_id,
            "start": slotStart,
            "responses": {
                "name": name,
                "email": email,
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



    
    def slots_from_calendar(self, calendar_api_key:str, event_id:str, slotStart:str):
        '''
        Get all the slots from the calendar for the given event id.
        Args:
            calendar_api_key (str): API key for Cal.com authentication
            event_id (str): The event id of the calendar that is to be set.
            slotStart (str): The start time of the slot to be booked
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
        
        
    def check_all_availabile_slots(self, calendar_api_key:str, event_id:str, slotStart:str):
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
            calendar_details = self.slots_from_calendar(calendar_api_key, event_id, slotStart)
            print("Checking all available slots with event id: ", event_id)
            print("\n\n Calendar details: ", calendar_details)
            return calendar_details
        except Exception as e:
            print(f"Error checking available slots: {str(e)}")
            return None



    def get_eventId_from_calendar(self, calendar_api_key:str, event_id:str, slotStart:str):
        '''
        Get all the event types from the calendar.
        Args:
            calendar_api_key (str): API key for Cal.com authentication
            event_id (str): The event id of the calendar that is to be set.
            slotStart (str): The start time of the slot to be booked
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

    def get_events_from_calendar(self, calendar_api_key:str, event_id:str, slotStart:str):
        '''
        Use this function to get all the events from the calendar.
        Args:
            context_variables (dict): A dictionary containing booking context information.
                - calendar_api_key (str): API key for Cal.com authentication
                - event_id (int, optional): The identifier of the event type being booked, it is eventtypes id  
                - slotStart (str, optional): The start time of the slot to be booked
        '''
        print("\n\n Getting events from calendar with api key: ", calendar_api_key)

        # Get all events from calendar
        event_details = self.get_eventId_from_calendar(calendar_api_key, event_id, slotStart)
        if event_details and len(event_details["event_types"]) > 0:
            # Store first event ID in context but return full details
            self.event_id = event_details["event_types"][0]["id"]
            print("\n\n Event id: ", self.event_id)
            return event_details
        return None
        

    def reserve_slot_for_startTime(self, calendar_api_key:str, event_id:str, slotStart:str):
        '''
        Use this function to reserve a slot for the given event id.
        Args:
            context_variables (dict): A dictionary containing booking context information.
                - calendar_api_key (str): API key for Cal.com authentication
                - event_id (int): The Cal.com event type ID
                - slotStart (str): ISO formatted start time for the slot to reserve
        '''
        print("Reserving slot with event id:", self.event_id)
        
        url = "https://api.cal.com/v2/slots/reservations"
        headers = {
            "Authorization": f"Bearer {calendar_api_key}",
            "Content-Type": "application/json",
            "cal-api-version": "2024-09-04"
        }
        payload = {
            "eventTypeId": self.event_id,
            "slotStart": self.slotStart
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