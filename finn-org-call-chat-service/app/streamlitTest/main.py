from swarm import Swarm, Agent
import json
from openai import OpenAI

# Initialize OpenAI client
openai_client = OpenAI(api_key="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")

# Initialize Swarm client with OpenAI client
client = Swarm(openai_client)

def get_calendar_details():
    return """
        # May 2025 Tech Calendar

        | Date       | Time        | Status      | Details                                     |
        |------------|-------------|-------------|---------------------------------------------|
        | May 1      | 09:00-10:30 | Available   |                                             |
        | May 1      | 13:00-14:00 | *BOOKED*  | Kubernetes cluster upgrade                  |
        | May 1      | 15:00-16:30 | Available   |                                             |
        | May 2      | 10:00-11:00 | Available   |                                             |
        | May 2      | 14:00-15:30 | *BOOKED*  | Code review session for API refactoring     |
        | May 5      | 09:30-11:00 | Available   |                                             |
        | May 5      | 13:00-15:00 | *BOOKED*  | React component library workshop            |
        | May 6      | 11:00-12:00 | Available   |                                             |
        | May 6      | 14:00-16:00 | Available   |                                             |
        | May 7      | 09:00-10:00 | *BOOKED*  | Docker optimization call                    |
        | May 7      | 13:30-14:30 | Available   |                                             |
        | May 8      | 10:00-12:00 | Available   |                                             |
        | May 8      | 15:00-16:00 | *BOOKED*  | GraphQL schema design meeting               |
        | May 9      | 09:00-10:30 | Available   |                                             |
        | May 9      | 14:00-15:00 | *BOOKED*  | AWS infrastructure security audit           |
        | May 12     | 11:00-12:30 | Available   |                                             |
        | May 12     | 15:30-17:00 | *BOOKED*  | PostgreSQL performance tuning session       |
        | May 13     | 09:00-11:00 | Available   |                                             |
        | May 13     | 13:00-14:30 | *BOOKED*  | Machine learning model review               |
        | May 14     | 10:00-12:00 | Available   |                                             |
        | May 14     | 14:00-15:00 | Available   |                                             |
        | May 15     | 09:30-11:00 | *BOOKED*  | CI/CD pipeline troubleshooting              |
        | May 15     | 13:00-14:30 | Available   |                                             |
        | May 16     | 11:00-12:00 | *BOOKED*  | Microservice architecture planning          |
        | May 16     | 15:00-16:30 | Available   |                                             |
    """

workflow = {
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

def check_calendar_availability(time_range: str):
    """
    Get the calendar details and find the best available time slot for a call or meeting. If the requested time range is not available, suggest alternative available time slots from the calendar. Only suggest times marked as 'Available'.
    """
    cal = get_calendar_details()
    find_best_time_agent = Agent(
        name="Find Best Time Agent",
        instructions="Analyze the calendar details and find the best available time slot for a call. If the requested time range is not available, suggest alternative available time slots from the calendar. Only suggest times marked as 'Available'.",
    )
    response = client.run(
        agent=find_best_time_agent,
        messages=[{"role": "user", "content": f"Calendar details: {cal}\nTime range: {time_range}"}],
    )
    return response.messages[-1]["content"]

agent_a = Agent(
    name="Calling Agent",
    instructions=f"""
        You are an AI assistant strictly following a directed workflow to guide the conversation. Below is the workflow you must adhere to:

        Workflow:
        {json.dumps(workflow, indent=2)}

        Relevant Information:
        ###### How To Effortlessly

        # Supercharge your  Call Operations with Voice AI

        Build a no-code AI phone call system with our AI voice agents:

        stop missing calls and start converting more leads.

        [Join beta](https://www.hirefinn.ai/bookademo) [Book a Demo](https://www.hirefinn.ai/bookademo)

        ![finnai preview landing](https://www.hirefinn.ai/_static/homepage/finn-prelanding-page.svg)

        ## Powering GROWING COMPANIES VOICE CALLS in 30+ countries

        [![rocketsdr](https://www.hirefinn.ai/_static/homepage/rocketsdr.svg)](https://neon.tech/)[![orbitwallet](https://www.hirefinn.ai/_static/homepage/orbitwallet.svg)](https://www.hirefinn.ai/)[![pillarbridgesolutions](https://www.hirefinn.ai/_static/homepage/pillarbridgesolutions.svg)](https://www.hirefinn.ai/)[![snazzy](https://www.hirefinn.ai/_static/homepage/snazzy.svg)](https://www.hirefinn.ai/)[![snazzy](https://www.hirefinn.ai/_static/homepage/frinks.svg)](https://www.hirefinn.ai/)

        ![team mates](https://www.hirefinn.ai/_static/homepage/trainingmade-easy.svg)

        ## Effortless Scalability

        Effortlessly handle millions of calls with scalable concurrent calling.

        ![team mates](https://www.hirefinn.ai/_static/homepage/intelligence.svg)

        ## Fully Compliant Platform

        We take data protection seriously. We're HIPAA, GDPR, and ISO 27001 compliant, and SOC 2 Type II is underway.

        ![team mates](https://www.hirefinn.ai/_static/homepage/teammate.svg)

        ## Ready-made Templates

        Tailor to your needs and start handling calls right away.

        ## Built-in Workflows    Just for You

        Book meetings, transfer to a human, detect voicemail, and more.

        ![team mates](https://www.hirefinn.ai/_static/homepage/training-done.svg)

        ## Seamlessly Integrate with Your Tech Stack

        With native and external connectivity to any CRM, telephony, automation platform, and database.

        ![team mates](https://www.hirefinn.ai/_static/homepage/integration-simple.svg)

        ![Agent configuration step 1](https://www.hirefinn.ai/_static/homepage/slider1.svg)

        ![Agent configuration step 2](https://www.hirefinn.ai/_static/homepage/slider2.svg)

        ![Agent configuration step 3](https://www.hirefinn.ai/_static/homepage/slider3.svg)

        ![Agent configuration step 4](https://www.hirefinn.ai/_static/homepage/slider4.svg)

        # Your Path to Success

        ## Easily tailor and deploy AI

        ## voice agents for your business

        01

        ### Build

        Tailor to your needs via choosing a language, picking a voice, and connecting to your knowledge base.

        02

        ### Test

        Perform comprehensive agent testing with built-in test LLM features to ensure seamless handling of edge cases.

        03

        ### Deploy

        Easily deploy your agents to phone calls, web calls, SMS, and more.

        04

        ### Monitor

        Track success rates, latency, and user sentiment through call history dashboard. Quickly identify failed calls.

        Use Cases

        ## Transform Customer Interactions with  AI-Powered Voice Agents

        Automate key business functions like receptionist services, appointment scheduling, lead qualification,

        surveys, customer support, and debt collection—enhancing efficiency and engagement.

        ![Receptionist](https://www.hirefinn.ai/_static/homepage/1.svg)

        ![Receptionist](https://www.hirefinn.ai/_static/homepage/case1.svg)

        Receptionist - Handling incoming calls and directing them appropriately.

        ![Appointment Setter](https://www.hirefinn.ai/_static/homepage/2.svg)

        ![Appointment Setter](https://www.hirefinn.ai/_static/homepage/case2.svg)

        Appointment Setter - Scheduling and managing appointments.

        ![Lead Qualification](https://www.hirefinn.ai/_static/homepage/3.svg)

        ![Lead Qualification](https://www.hirefinn.ai/_static/homepage/case3.svg)

        Lead Qualification - Assessing and categorizing potential customers.

        ![Survey](https://www.hirefinn.ai/_static/homepage/4.svg)

        ![Survey](https://www.hirefinn.ai/_static/homepage/case4.svg)

        Survey - Conducting automated surveys to gather feedback.

        ![Customer Service](https://www.hirefinn.ai/_static/homepage/5.svg)

        ![Customer Service](https://www.hirefinn.ai/_static/homepage/case5.svg)

        Customer Service - Addressing customer inquiries & support requests.

        ![Debt Collection](https://www.hirefinn.ai/_static/homepage/6.svg)

        ![Debt Collection](https://www.hirefinn.ai/_static/homepage/case6.svg)

        Debt Collection - Automating follow-ups for overdue payments.

        #### Testimonials

        ## What Our Clients Say

        Transforming Call Operations with Proven Results

        ![Ayush Pateria](https://www.hirefinn.ai/_static/homepage/c1.svg)

        #### Ayush Pateria

        CEO & Cofounder, Snazzy

        Our early adoption of Finn AI, combined with our ability to customize it deeply, has given us a competitive edge. With a 3x increase in profitability per lead and a 25% higher call success rate compared to human agents, our call campaigns are more effective than ever.

        ![David Johnson](https://www.hirefinn.ai/_static/homepage/c2.svg)

        #### David Johnson

        Head of HR, Frinks AI

        Integrating Finn AI into our assessment tool took less than two days and resulted in a 70% reduction in false-positive assessments. The platform's ease of integration and robust feature set have transformed our hiring process.

        ![Shivansh](https://www.hirefinn.ai/_static/homepage/c3.svg)

        #### Shivansh

        Head of Engineering, RocketSDR

        Integrating Finn AI was remarkably fast—completed in under two days—and it delivered a 70% reduction in false-positive assessments. The platform is packed with features that are easy to integrate and truly enhance our evaluation process.

        ![Alice Smith](https://www.hirefinn.ai/_static/homepage/c4.svg)

        #### Alice Smith

        Senior Engineer, Gofts

        Our numbers show that 45-50% of calls are completely resolved by Finn AI without ever touching a human. This has not only streamlined our operations but also ensured that patients receive prompt, effective support.

        ![Shikha Chouksey](https://www.hirefinn.ai/_static/homepage/c5.svg)

        #### Shikha Chouksey

        COO & Cofounder, Orbit Wallet

        We were able to contain 65% of voice calls with the bot—calls that used to go directly to manual agents. This efficiency boost has saved us more than 600 man hours per month and significantly reduced call wait times.

        ![Rajesh Bangera](https://www.hirefinn.ai/_static/homepage/c6.svg)

        #### Rajesh Bangera

        Founder, PBS

        Finn AI offers an incredible platform that has streamlined our customer service operations and drastically improved engagement. With fast, reliable voice agents handling routine inquiries, our team can focus on strategic, higher-value tasks.

        ## Hire FinnAI and

        ## Effortlessly Deploy AI Calls

        Discuss Your Use Case

        ### Fort-nightly Launches

        We move quickly and get you what you need

        ### Powerful Tools

        Pre-built dashboards, reports, automations, more

        Test Mode

        [iframe](https://api.razorpay.com/v1/checkout/public?traffic_env=production&build=2044d2c9828789bc7f5a6d3360e751b1b558638d&build_v1=368703ca18df4bd6071ae944791cd8870683687b&checkout_v2=1&new_session=1)

        Instructions:
        - Analyze the chat history to determine the current task and conversation context
        - Based on the current task node in the workflow, follow these steps:
            1. If contentType is "Static", use the exact content as the response
            2. If contentType is "Prompt", generate a contextual response using the content guidelines
        - Evaluate the user's response sentiment and intent
        - Use the workflow edges to determine the next appropriate task:
            * Match the edge conditions against the user's response
            * Transition to the corresponding "to" node when conditions are met
        - Stay strictly within the defined workflow paths
    """,
    functions=[check_calendar_availability] 
)

import streamlit as st

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Set up the Streamlit UI
st.title("AI Call Assistant")
st.subheader("Chat with our AI representative")
# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user input
user_input = st.chat_input("Type your message here...")

# Process user input when submitted
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Send the entire chat history to the agent
            response = client.run(
                agent=agent_a,
                messages=st.session_state.chat_history,
            )
            ai_response = response.messages[-1]["content"]
            st.write(ai_response)
    
    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content":ai_response})