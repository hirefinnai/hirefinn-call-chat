import streamlit as st
import requests
from typing import List, Dict
import json
import asyncio
from agents_worker.main import HireFinnAgent

st.title("HireFinn Call Chat Interface")

# Initialize session state for messages if not exists
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar inputs
with st.sidebar:
    st.header("Configuration")
    org_id = st.text_input("Organization ID", "org_123")
    agent_id = st.text_input("Agent ID", "agent_456") 
    use_case = st.text_input("Use Case", "customer_support")
    language = st.selectbox("Language", ["English", "Spanish", "French", "German"], index=0)
    identity_text = st.text_area("Identity Text", "User is a premium customer.")
    guardrails = st.text_area("Guardrails", "Be concise and professional.")
    response_guidelines = st.text_area("Response Guidelines", "Answer within 3 sentences.")
    welcome_message = st.text_area("Welcome Message", "Welcome to HireFinn!")
    
    # Call workflow input as JSON
    default_workflow = {
        "nodes": [
            {
                "id": "Task1",
                "name": "Greetings",
                "content": "say 'Hello, this is John, An AI representative calling from Omega HMS Healthcare organization. I'm reaching out to help you access your health service portal, May I speak with Akarsh, please?'",
                "contentType": "Static"
            },
            {
                "id": "Task2", 
                "name": "Check Calendar availability",
                "content": "1. Ask user when they are available for the tour.\n2. Call function check_calendar_availability to check for availability in the user provided time range.",
                "contentType": "Prompt"
            },
            {
                "id": "Task3",
                "name": "Winding Up", 
                "content": "say 'Thank you for your time. If you have any further questions, feel free to reach out to us. Have a great day! Goodbye!'",
                "contentType": "Static"
            }
        ],
        "edges": [
            {
                "from": "Task1",
                "to": "Task2",
                "condition": "user said yes or shows interests"
            },
            {
                "from": "Task1",
                "to": "Task3",
                "condition": "user is a bit hesitant or has no interest"
            },
            {
                "from": "Task2",
                "to": "Task3",
                "condition": "user is a bit hesitant or has no interest"
            }
        ]
    }
    workflow_json = st.text_area(
        "Call Workflow (JSON)",
        value=json.dumps(default_workflow, indent=2),
        height=200
    )
    try:
        call_workflow = json.loads(workflow_json)
    except json.JSONDecodeError:
        st.error("Invalid JSON format for workflow")
        call_workflow = {"nodes": [], "edges": []}

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Prepare the request
    request_data = {
        "messages": st.session_state.messages,
        "org_id": org_id,
        "agent_id": agent_id,
        "use_case": use_case,
        "language": language,
        "indentity_text": identity_text,
        "guardrails": guardrails,
        "response_guidelines": response_guidelines,
        "welcome_message": welcome_message,
        "call_workflow": call_workflow
    }

    # Make API call
    try:
        worker = HireFinnAgent()
        # Run async code in sync context
        assistant_response = asyncio.run(worker.get_assistant_response(
            request_data["messages"],
            request_data["org_id"], 
            request_data["agent_id"],
            request_data["messages"][-1]["content"] if request_data["messages"] else "",
            request_data["use_case"],
            request_data["language"],
            request_data["indentity_text"],
            request_data["guardrails"], 
            request_data["response_guidelines"],
            request_data["welcome_message"],
            request_data["call_workflow"]
        ))

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.write(assistant_response)
    except Exception as e:
        st.error(f"Error communicating with the server: {str(e)}")
