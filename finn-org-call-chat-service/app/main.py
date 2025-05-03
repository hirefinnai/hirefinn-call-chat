from agents_worker.main import HireFinnAgent
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

# Model for chat messages
class ChatMessage(BaseModel):
    role: str
    content: str

# Model for chat request
class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    org_id: str = ""
    agent_id: str = ""
    use_case: str = ""
    language: str = ""
    indentity_text: str = ""
    guardrails: str = ""
    response_guidelines: str = ""
    welcome_message: str = ""
    call_workflow: dict = {}

# Model for chat response  
class ChatResponse(BaseModel):
    response: str
    
@app.post("/v1/call_chat/query", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        worker = HireFinnAgent()
        assistant_response = await worker.get_assistant_response(
            request.messages,
            request.org_id,
            request.agent_id,
            request.messages[-1].content if request.messages else "",
            request.use_case,
            request.language,
            request.indentity_text,
            request.guardrails,
            request.response_guidelines,
            request.welcome_message,
            request.call_workflow
        )
        return ChatResponse(response=assistant_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    host = os.getenv("CALL_CHAT_SERVICE_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("CALL_CHAT_SERVICE_SERVER_PORT", 7501))
    uvicorn.run(app, host=host, port=port)