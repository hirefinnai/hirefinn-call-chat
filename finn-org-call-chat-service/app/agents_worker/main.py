from swarm import Swarm
from openai import OpenAI
from rag_content.main import RagContent
import json
from swarm import Agent
from tools.check_availability.main import transfer_to_check_availability
from tools.calendar_details.main import transfer_to_calendar_details
from tools.book_appointment.main import transfer_to_book_appointment
from tools.get_workflow.main import transfer_to_get_workflow

# Initialize OpenAI client
openai_client = OpenAI(api_key="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")

# Initialize Swarm client with OpenAI client
client = Swarm(openai_client)



class HireFinnAgent:
    def __init__(self):
        self.rag_content=""
        self.agent = Agent(
            name="Hire Finn Interface Agent",
            instructions="""You are a sophisticated calendar management assistant with access to multiple specialized tools for handling appointment scheduling and calendar operations.

                Your primary responsibilities include:
                1. Managing calendar availability checks using transfer_to_check_availability
                2. Retrieving calendar details using transfer_to_calendar_details 
                3. Booking appointments using transfer_to_book_appointment
                4. Following workflow protocols using transfer_to_get_workflow

                When interacting with users:
                - First get the workflow using transfer_to_get_workflow to understand the conversation flow
                - When a user requests to book an appointment:
                1. Use transfer_to_calendar_details to get current calendar information
                2. Use transfer_to_check_availability to verify if the requested time slot is available
                3. If the slot is available, use transfer_to_book_appointment to schedule the appointment
                4. If the slot is not available, inform the user and suggest alternative available times

                Important guidelines:
                - Always verify calendar availability before attempting to book
                - Provide clear feedback about booking status
                - If a requested slot is unavailable, proactively suggest alternatives
                - Follow the workflow structure for maintaining conversation flow
                - Be courteous and professional in all interactions

                Remember to use the appropriate tool for each task:
                - transfer_to_check_availability for checking time slot availability
                - transfer_to_calendar_details for accessing calendar information
                - transfer_to_book_appointment for finalizing bookings
                - transfer_to_get_workflow for conversation flow guidance""",
                
                functions=[transfer_to_check_availability, transfer_to_calendar_details, transfer_to_book_appointment, transfer_to_get_workflow]
            )

    async def extract_rag_content(self, org_id, agent_id, user_input):
        rag_worker = RagContent()
        self.rag_content = await rag_worker.get_rag_content(org_id=org_id , agent_id=agent_id, query=user_input)

        print("RAG content: ", self.rag_content)
        return self.rag_content


    async def get_assistant_response(self, messages, org_id, agent_id, user_input):
        assistant_response = "Response from assistant"

        rag_content = await self.extract_rag_content(org_id=org_id, agent_id=agent_id, user_input=user_input)

        assistant_response = client.run(
            agent = self.agent,
            messages = messages,
            debug = True
        )

        print("Assistant response: ", assistant_response)
        print("Name of the agent: ", self.agent.name)
        return assistant_response.messages[-1]["content"]



