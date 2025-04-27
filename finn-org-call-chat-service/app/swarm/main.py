from agents import Agent
from agents import Runner
from functions import get_weather
from swarm.instructions import USER_INTERFACE_INSTRUCTIONS
from rag_content.main import RagContent

class HireFinnAgent:
    def __init__(self):
        self.rag_content=""

        self.agent = Agent(
            name="HireFinn Agent",
            instructions=USER_INTERFACE_INSTRUCTIONS,
            model="gpt-3.5-turbo"

        )

    def user_interface_agent(self):
        return self.agent
    

    async def call_chat_completion(self, query: str, messages: list, agent_id: str, org_id: str):
        
        rag_content = RagContent()
        self.rag_content = await rag_content.get_rag_content(query, agent_id, org_id)

        print("RAG CONTENT: ", self.rag_content)
        self.agent.instructions = USER_INTERFACE_INSTRUCTIONS.format(rag_content=self.rag_content, query=query)

        response = await Runner.run(self.agent,
                              input=query
                              )
        print("AI Response: ", response)

        return response



