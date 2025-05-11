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
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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


    async def get_assistant_response(self, messages,  calendar_api_key, org_id, agent_id, user_input, use_case, language, indentity_text, guardrails, response_guidelines, welcome_message, call_workflow, finn_name):
        assistant_response = "Response from assistant"

        rag_content = await self.extract_rag_content(org_id=org_id, agent_id=agent_id, user_input=user_input)
        
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
            rag_content=rag_content,
            finn_name=finn_name
        )
    
        # Update agent instructions
        self.instructions = instructions
        # Get response from agent

        assistant_response = client.run(
            agent = self.agent,
            messages = messages,
            debug = True,
            context_variables={"calendar_api_key": self.calendar_api_key, "event_id": 2444587, "slotStart": "2025-05-14T16:00:00.000Z"}
        )

        # print("\n\n Assistant response: ", assistant_response)
        # print("\n\n Context variables: ", )
        print("\n\n Name of the agent: ", self.agent.name)
        return assistant_response.messages[-1]["content"]



