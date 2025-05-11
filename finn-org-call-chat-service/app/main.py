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
    finn_name: str = "Voice Agent"
    calendar_api_key: str = ""

# Model for chat response  
class ChatResponse(BaseModel):
    response: str
    
@app.post("/v1/call_chat/query", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        worker = HireFinnAgent()
        print("Request: ", request)
        assistant_response = await worker.get_assistant_response(
            messages=request.messages,
            calendar_api_key=request.calendar_api_key,
            org_id=request.org_id,
            agent_id=request.agent_id,
            user_input=request.messages[-1].content if request.messages else "",
            use_case=request.use_case,
            language=request.language,
            indentity_text=request.indentity_text,
            guardrails= request.guardrails,
            response_guidelines=request.response_guidelines,
            welcome_message=request.welcome_message,
            call_workflow=request.call_workflow,
            finn_name=request.finn_name
        )
        return ChatResponse(response=assistant_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    host = os.getenv("CALL_CHAT_SERVICE_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("CALL_CHAT_SERVICE_SERVER_PORT", 7501))
    uvicorn.run(app, host=host, port=port)