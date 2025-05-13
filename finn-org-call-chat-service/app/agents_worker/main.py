from swarm import Swarm
from openai import OpenAI
from rag_content.main import RagContent
import json
from swarm import Agent
from agents_worker.agents.workflow_agent import to_get_workflow_agent
from agents_worker.instructions import generate_call_agent_prompt
from agents_worker.agents.calendar_agent import to_calendar_agent
import os

# Initialize OpenAI client
openai_client = OpenAI(api_key="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")

# Initialize Swarm client with OpenAI client
client = Swarm(openai_client)

class HireFinnAgent:
    def __init__(self):
        self.rag_content=""
        self.instructions=""
        self.calendar_api_key=""
        self.agent = Agent(
            name="Finn Interface Agent",
            instructions=self.instructions,
            functions=[to_calendar_agent],         ## Remember to add Transfer to Human Agent
            parallel_tool_calls=True,
            )

    async def extract_rag_content(self, org_id, agent_id, user_input):
        rag_worker = RagContent()
        self.rag_content = await rag_worker.get_rag_content(org_id=org_id , agent_id=agent_id, query=user_input)

        print("RAG content: ", self.rag_content)
        return self.rag_content

    async def get_assistant_response(self,  messages, calendar_api_key, org_id, agent_id, user_input, use_case, language, indentity_text, guardrails, response_guidelines, welcome_message, call_workflow, finn_name):
        print("Calendar API key: ", calendar_api_key)
        self.calendar_api_key = calendar_api_key    
        
        # Generate dynamic instructions using the prompt function
        instructions = generate_call_agent_prompt(
            messages=messages,
            org_id=org_id,
            latest_user_input=user_input,
            use_case=use_case,
            language=language,
            identity_text=indentity_text,
            guardrails=guardrails,
            response_guidelines=response_guidelines,
            welcome_message=welcome_message,
            call_workflow=call_workflow,
            rag_content="",
            finn_name=finn_name
        )

        # Add sentiment analysis instruction
        sentiment_instruction = """
        For every user input, you must:
        1. Analyze the sentiment of the user's message
        2. Assign a sentiment score from 1 to 5 where:
           - 1: Very Negative
           - 2: Negative
           - 3: Neutral
           - 4: Positive
           - 5: Very Positive
        3. Return your response in this exact format:
        {
            "response": "your response message here",
            "sentiment": sentiment_score_here
        }
        
        The sentiment score should be based on:
        - Word choice and tone
        - Emotional content
        - Context of the conversation
        - User's apparent satisfaction level
        """
        
        self.instructions = instructions + "\n" + sentiment_instruction
        self.agent.instructions = self.instructions
        
        # Get response from agent
        assistant_response = client.run(
            agent=self.agent,
            messages=messages,
            debug=True,
            context_variables={"calendar_api_key": self.calendar_api_key, "event_id": 2444587, "slotStart": "2025-06-15T15:15:00.000Z"}
        )

        response_content = assistant_response.messages[-1]["content"]
        print("Response content: ", response_content)
        try:
            # Try to parse the response as JSON
            response_data = json.loads(response_content)
            if isinstance(response_data, dict) and "response" in response_data and "sentiment" in response_data:
                print("Response data with sentiment: ", response_data)
                return response_data
        except:
            # If parsing fails, return a default format
            return {
                "response": response_content,
                "sentiment": 3  # Default neutral sentiment
            }



