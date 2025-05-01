import asyncio
import aiohttp



class RagContent:
    def __init__(self):
        self.rag_content = ""


    async def get_rag_content(self, query: str="", agent_id: str="", org_id: str=""):
        """
        Make an async HTTP request to the v1/query endpoint
        to get the RAG content.
        
        Args:
            query (str): The query string
            agent_id (str): The agent ID
            org_id (str): The organization ID
            
        Returns:
            dict: The JSON response from the server
        """
 
        url = "https://rag-api.hirefinn.ai/v1/query"

        data= aiohttp.FormData()
        data.add_field("query", query)
        data.add_field("agent_id", agent_id)
        data.add_field("org_id", org_id)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    self.rag_content = await response.json()
                else:
                    raise Exception(f"Request failed with status {response.status}: {await response.text()}")

        return  self.rag_content


if __name__ == "__main__":
    print("rag_content")
    async def main():
        rag_content= RagContent()
        # data= await rag_content.get_rag_content("What is game mchanics?", "e318c8f0-7e4b-4b25-ad29-2babf0efefa7", "7f15dc26-851a-4653-a779-7b9d720543ec")
        data="Hello"
        print(data)
        return data

    asyncio.run(main())