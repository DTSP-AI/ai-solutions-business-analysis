# -*- coding: utf-8 -*-
# File: C:\AI_src\marketing-assistant\ai_marketing_assistant.py

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    st.error("🔑 OPENAI_API_KEY not set in environment!")
    st.stop()

# Configure page
st.set_page_config(page_title="AI Business Optimization Intake", layout="wide")

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7, openai_api_key=openai_key)

# Sidebar: Business Profile
st.sidebar.header("📋 Business Intake Form")
user_name      = st.sidebar.text_input("Your Name")
business_name  = st.sidebar.text_input("Business Name")
website        = st.sidebar.text_input("Business Website")
industry       = st.sidebar.selectbox("Industry", ["Jewelry", "Med Spa", "Real Estate", "Fitness", "Other"])
location       = st.sidebar.text_input("Location")
annual_revenue = st.sidebar.number_input("Annual Revenue (USD)", min_value=0, step=1000, value=0)
employees      = st.sidebar.number_input("Number of Employees", min_value=0, step=1, value=0)

# Main title
st.title("🧠 AI Solutions Discovery & Optimization Intake")
st.write(
    f"Welcome {user_name} — let's break down your current systems and find "
    "the highest ROI opportunities for automation and AI integration."
)

# Sales & Operations
st.subheader("🧰 Sales & Operations")
sales_process   = st.text_area("Describe your current sales process:")
lead_tools      = st.text_area("What tools do you currently use for leads and appointments?")
has_crm         = st.selectbox("Do you use a CRM?", ["Yes", "No"])
crm_name        = st.text_input("Which CRM do you use (if any)?")
booking_process = st.text_area("How are appointments currently booked?")
follow_up       = st.text_area("How do you track follow-ups or missed leads?")

# Marketing
st.subheader("📣 Marketing")
channels             = st.multiselect("Active Marketing Channels", ["Google Ads", "Meta Ads", "TikTok", "SEO", "Influencer", "Referral", "Events"])
lead_routing         = st.text_area("How are leads captured and routed?")
lead_action          = st.text_area("Describe what happens after a lead comes in:")
existing_automations = st.text_area("Any automations currently in place?")

# Engagement & Retention
st.subheader("📞 Engagement & Retention")
sales_cycle       = st.slider("Average Sales Cycle (days)", min_value=1, max_value=180, value=30)
follow_up_tactics = st.text_area("How do you follow up with missed calls, abandoned carts, or no-shows?")
retention         = st.text_area("Any current loyalty, membership, or re-engagement programs?")

# AI & Automation Readiness
st.subheader("🤖 AI & Automation Readiness")
uses_ai          = st.selectbox("Are you using AI currently?", ["Yes", "No"])
ai_tools         = st.text_area("If yes, describe your AI tools or setup.")
manual_areas     = st.multiselect("Where do you spend the most manual time?", ["Lead follow-up", "Appointment setting", "Content creation", "Customer questions"])
dream_automation = st.text_area("What would you automate tomorrow if it worked perfectly?")

# Tech Stack
st.subheader("⚙️ Tech Stack")
tools      = st.multiselect("Current Tools in Use", ["Calendly", "Shopify", "Squarespace", "Twilio", "Stripe", "Zapier", "Klaviyo", "Mailchimp", "GoHighLevel"])
api_access = st.selectbox("Do you have admin/API access to these tools?", ["Yes", "No", "Not sure"])
comms      = st.selectbox("Preferred customer communication method:", ["Text", "Email", "Phone", "DMs", "Website Chat"])

# Goals & Timeline
st.subheader("🌟 Goals & Timeline")
goals           = st.text_area("Top 3 revenue goals (next 6 months):")
biggest_problem = st.text_area("What’s the #1 problem you're trying to solve right now?")
comfort         = st.selectbox("Comfort level with automation/AI:", ["Bring on the robots", "Need guidance", "Start simple"])
engagement      = st.selectbox("Preferred engagement model:", ["Done-For-You", "Hybrid", "DIY with Support"])
timeline        = st.selectbox("Implementation timeline:", ["<30 days", "30-60 days", "60-90 days", "Flexible"])

# Generate client & dev report
if st.button("🧠 Generate Full Report & Scope"):
    with st.spinner("Generating client-facing report and development scope..."):
        try:
            # Build intake summary
            intake_summary = {
                "Client Name": user_name,
                "Business Name": business_name,
                "Website": website,
                "Industry": industry,
                "Location": location,
                "Annual Revenue": annual_revenue,
                "Employees": employees,
                "Sales Process": sales_process,
                "Lead Tools": lead_tools,
                "CRM": crm_name if has_crm == "Yes" else "None",
                "Booking Process": booking_process,
                "Follow-Up Process": follow_up,
                "Marketing Channels": channels,
                "Lead Routing": lead_routing,
                "Post Lead Actions": lead_action,
                "Existing Automations": existing_automations,
                "Sales Cycle (days)": sales_cycle,
                "Retention Programs": retention,
                "AI Usage": ai_tools if uses_ai == "Yes" else "None",
                "Manual Effort Areas": manual_areas,
                "Dream Automation": dream_automation,
                "Tech Tools": tools,
                "API Access": api_access,
                "Communication": comms,
                "Goals": goals,
                "Biggest Problem": biggest_problem,
                "Comfort Level": comfort,
                "Engagement Model": engagement,
                "Timeline": timeline
            }

            # Anti-hallucination system prompt
            system_prompt = (
                "You are a Senior AI Solutions Architect and Consultant. "
                "Speak only in crystal-clear bullet points. Never hallucinate—only use facts from the intake JSON. "
                "If you lack data, say 'Insufficient data' rather than guessing. "
                "Output must be so structured that a chimpanzee could read it on his phone speeding down the highway with a female chimpanzee in his lap."
            )

            # Structured user prompt
            user_prompt = (
                "First, generate the Client-Facing Report with sections:\n"
                "1. Executive Summary (1–2 sentences)\n"
                "2. Current System Snapshot (bullets)\n"
                "3. Key Challenges (top 3 bullets)\n"
                "4. Opportunities & Recommendations (prioritized bullets)\n"
                "5. Next Steps for the Client (3 non-technical actions with deadlines)\n\n"
                "Then, generate the Dev Implementation Scope with sections:\n"
                "A. Phase Plan as table: Phase | Task | Deliverable | Owner | Effort (hrs) | Timeline (weeks)\n"
                "B. Tech Stack Details: list GHL workflows, Vapi agent roles, Twilio flows\n"
                "C. Anti-BS Validation: list checks to prevent hallucinations and ensure QA\n\n"
                f"Here is the intake JSON:\n{intake_summary}"
            )

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            # Call LLM
            response = llm(messages)

            # Display
            st.subheader("📋 Client-Facing Report & Dev Implementation Scope")
            st.markdown(response.content)

        except Exception as e:
            st.error("❌ Failed to generate the report & scope.")
            st.code(str(e))
