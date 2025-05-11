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
    CALENDAR_API_KEY = st.text_input("Calendar API Key", "cal_live_349fa2e7b5e16684b3f89915cc17f356")
    org_id = st.text_input("Organization ID", "org_123")
    agent_id = st.text_input("Agent ID", "agent_456") 
    use_case = st.text_input("Use Case", "Lead Generation")
    language = st.selectbox("Language", ["English", "Spanish", "French", "German"], index=0)
    identity_text = st.text_area("Identity Text", "User is a premium customer.")
    guardrails = st.text_area("Guardrails", "Be concise and professional.")
    response_guidelines = st.text_area("Response Guidelines", "Answer within 3 sentences.")
    welcome_message = st.text_area("Welcome Message", "Welcome to HireFinn!")
    finn_name = st.text_input("Finn Name", "John")
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
                "name": "Get Calendar Details",
                "content": "1. Call function get_events_from_calendar to retrieve event details and event ID\n2. Use event ID to get available event types and details",
                "contentType": "Prompt"
            },
            {
                "id": "Task3", 
                "name": "Check Availability",
                "content": "1. Ask user when they would like to schedule.\n2. Call function check_all_availabile_slots to check available time slots",
                "contentType": "Prompt"
            },
            {
                "id": "Task4",
                "name": "Reserve Slot", 
                "content": "Call function reserve_slot_for_startTime to reserve the selected time slot",
                "contentType": "Prompt"
            },
            {
                "id": "Task5",
                "name": "Book Appointment",
                "content": "Call function book_appointment_for_startTime to finalize the booking",
                "contentType": "Prompt"
            },
            {
                "id": "Task6",
                "name": "Winding Up",
                "content": "say 'Thank you for your time. Your appointment has been booked. If you have any questions, feel free to reach out. Have a great day! Goodbye!'",
                "contentType": "Static"
            }
        ],
        "edges": [
            {
                "from": "Task1",
                "to": "Task2",
                "condition": "user confirms identity"
            },
            {
                "from": "Task2", 
                "to": "Task3",
                "condition": "calendar details and event types retrieved successfully"
            },
            {
                "from": "Task3",
                "to": "Task4", 
                "condition": "suitable slot found"
            },
            {
                "from": "Task4",
                "to": "Task5",
                "condition": "slot reserved successfully"
            },
            {
                "from": "Task5",
                "to": "Task6",
                "condition": "appointment booked successfully"
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
        "calendar_api_key": CALENDAR_API_KEY,
        "org_id": org_id,
        "agent_id": agent_id,
        "use_case": use_case,
        "language": language,
        "indentity_text": identity_text,
        "guardrails": guardrails,
        "response_guidelines": response_guidelines,
        "welcome_message": welcome_message,
        "call_workflow": call_workflow,
        "finn_name": finn_name
    }

    # Make API call
    try:
        worker = HireFinnAgent()
        # Run async code in sync context
        assistant_response = asyncio.run(worker.get_assistant_response(
            request_data["messages"],
            request_data["calendar_api_key"],
            request_data["org_id"], 
            request_data["agent_id"],
            request_data["messages"][-1]["content"] if request_data["messages"] else "",
            request_data["use_case"],
            request_data["language"],
            request_data["indentity_text"],
            request_data["guardrails"], 
            request_data["response_guidelines"],
            request_data["welcome_message"],
            request_data["call_workflow"],
            request_data["finn_name"]
        ))

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.write(assistant_response)
    except Exception as e:
        st.error(f"Error communicating with the server: {str(e)}")
