from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from agents import Runner
from swarm.main import HireFinnAgent
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Create a single instance of HireFinnAgent to be used across requests
hire_finn_agent = HireFinnAgent()

# Define the request model
class ChatRequest(BaseModel):
    query: str
    messages: List[dict]
    agent_id: str
    org_id: str

@app.post("/v1/call/query")
async def call_query(request: ChatRequest):
    try:
        result = await hire_finn_agent.call_chat_completion(
            query=request.query,
            messages=request.messages,
            agent_id=request.agent_id,
            org_id=request.org_id
        )

        return {"response": result.final_output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8555)