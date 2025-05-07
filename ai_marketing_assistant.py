# -*- coding: utf-8 -*-
# Integrated AI Intake: Marketing + HAF + CII → OAB

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
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=openai_key)

# Sidebar: Business Profile
st.sidebar.header("📋 Business Intake Form")
user_name = st.sidebar.text_input("Your Name")
business_name = st.sidebar.text_input("Business Name")
website = st.sidebar.text_input("Business Website")
industry = st.sidebar.selectbox("Industry", ["Jewelry", "Med Spa", "Real Estate", "Fitness", "Other"])
location = st.sidebar.text_input("Location")
annual_revenue = st.sidebar.number_input("Annual Revenue (USD)", min_value=0, step=1000, value=0)
employees = st.sidebar.number_input("Number of Employees", min_value=0, step=1, value=0)

# Main title
st.title("🧠 AI Solutions Discovery & Optimization Intake")
st.write(f"Welcome {user_name} — let's break down your current systems and find the highest ROI opportunities for automation and AI integration.")

# Sales & Operations
st.subheader("🧰 Sales & Operations")
sales_process = st.text_area("Describe your current sales process:")
lead_tools = st.text_area("What tools do you currently use for leads and appointments?")
has_crm = st.selectbox("Do you use a CRM?", ["Yes", "No"])
crm_name = st.text_input("Which CRM do you use (if any)?")
booking_process = st.text_area("How are appointments currently booked?")
follow_up = st.text_area("How do you track follow-ups or missed leads?")

# Marketing
st.subheader("📣 Marketing")
channels = st.multiselect("Active Marketing Channels", ["Google Ads", "Meta Ads", "TikTok", "SEO", "Influencer", "Referral", "Events"])
lead_routing = st.text_area("How are leads captured and routed?")
lead_action = st.text_area("Describe what happens after a lead comes in:")
existing_automations = st.text_area("Any automations currently in place?")

# Engagement & Retention
st.subheader("📞 Engagement & Retention")
sales_cycle = st.slider("Average Sales Cycle (days)", min_value=1, max_value=180, value=30)
follow_up_tactics = st.text_area("How do you follow up with missed calls, abandoned carts, or no-shows?")
retention = st.text_area("Any current loyalty, membership, or re-engagement programs?")

# AI & Automation Readiness
st.subheader("🤖 AI & Automation Readiness")
uses_ai = st.selectbox("Are you using AI currently?", ["Yes", "No"])
ai_tools = st.text_area("If yes, describe your AI tools or setup.")
manual_areas = st.multiselect("Where do you spend the most manual time?", ["Lead follow-up", "Appointment setting", "Content creation", "Customer questions"])
dream_automation = st.text_area("What would you automate tomorrow if it worked perfectly?")

# Tech Stack
st.subheader("⚙️ Tech Stack")
tools = st.multiselect("Current Tools in Use", ["Calendly", "Shopify", "Squarespace", "Twilio", "Stripe", "Zapier", "Klaviyo", "Mailchimp", "GoHighLevel"])
api_access = st.selectbox("Do you have admin/API access to these tools?", ["Yes", "No", "Not sure"])
comms = st.selectbox("Preferred customer communication method:", ["Text", "Email", "Phone", "DMs", "Website Chat"])

# Goals & Timeline
st.subheader("🌟 Goals & Timeline")
goals = st.text_area("Top 3 revenue goals (next 6 months):")
biggest_problem = st.text_area("What’s the #1 problem you're trying to solve right now?")
comfort = st.selectbox("Comfort level with automation/AI:", ["Bring on the robots", "Need guidance", "Start simple"])
engagement = st.selectbox("Preferred engagement model:", ["Done-For-You", "Hybrid", "DIY with Support"])
timeline = st.selectbox("Implementation timeline:", ["<30 days", "30-60 days", "60-90 days", "Flexible"])

# HAF/CII Expanders
with st.expander("🔰 Advanced: Hierarchical Agent Framework (HAF)"):
    haf_roles = st.text_area("List critical roles and their main responsibilities")
    haf_workflows = st.text_area("Map your key workflows (e.g., Lead → Sale → Delivery)")
    haf_agents = st.text_area("Which tasks could be delegated to AI agents?")

with st.expander("🧩 Advanced: Cognitive Infrastructure Intake (CII)"):
    memory_needs = st.text_area("What memory or data history do agents need?")
    agent_tools = st.text_area("List specific APIs/tools needed for each agent")
    security = st.text_area("Any compliance or regulatory requirements?")
    latency_critical = st.text_area("Which processes must be real-time vs async?")

# Output
if st.button("🧠 Generate Full Report & Scope"):
    with st.spinner("Generating full strategic analysis + agent blueprint..."):
        try:
            full_input = {
                "user": user_name,
                "business": business_name,
                "industry": industry,
                "location": location,
                "website": website,
                "revenue": annual_revenue,
                "employees": employees,
                "sales_process": sales_process,
                "lead_tools": lead_tools,
                "crm_name": crm_name if has_crm == "Yes" else "None",
                "booking": booking_process,
                "followups": follow_up,
                "channels": channels,
                "lead_routing": lead_routing,
                "post_lead": lead_action,
                "automations": existing_automations,
                "sales_cycle": sales_cycle,
                "retention": retention,
                "ai_use": ai_tools if uses_ai == "Yes" else "None",
                "manual_time": manual_areas,
                "dream_automation": dream_automation,
                "tech": tools,
                "api_access": api_access,
                "comms": comms,
                "goals": goals,
                "problem": biggest_problem,
                "comfort": comfort,
                "engagement": engagement,
                "timeline": timeline,
                "HAF_roles": haf_roles,
                "HAF_workflows": haf_workflows,
                "HAF_agents": haf_agents,
                "CII_memory": memory_needs,
                "CII_tools": agent_tools,
                "CII_compliance": security,
                "CII_latency": latency_critical
            }

            system_prompt = (
                "You are a Senior AI Architect and Strategist. Use the intake JSON below to generate three deliverables:\n"
                "1. A client-facing report\n" 
                "2. A developer-facing implementation scope\n"
                "3. A full Organizational Agent Blueprint (OAB) using LangGraph structure.\n"
                "Respond ONLY with structured output. Do not guess. Use exact inputs."
            )

            user_prompt = f"""
            First, summarize the client situation with:
            - Executive Summary
            - Current Systems Overview
            - Top Challenges
            - Automation Opportunities
            - Next 3 Suggested Steps

            Second, output a Developer Implementation Scope:
            - Table: Phase | Task | Deliverable | Owner | Effort (hrs) | Timeline (weeks)
            - Toolchain Mapping
            - Validation Protocols

            Third, output a complete Organizational Agent Blueprint (OAB) using this input. 
Format it EXACTLY in the XML-style block format that Kodey agents use:
<description>...</description>
<notes>...</notes>
<actions>...</actions>

Each agent should include all 3 sections clearly separated. Include the Supervisor Agent and at least 3-5 Executive Agents.
Wrap the entire OAB section in triple backticks with 'xml' so it renders as a copy-pasteable code block.
            {full_input}
            """

            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            response = llm(messages)

            st.subheader("📋 Full Strategic Report + OAB")
            st.markdown(response.content)

        except Exception as e:
            st.error("❌ Failed to generate the full report.")
            st.code(str(e))
