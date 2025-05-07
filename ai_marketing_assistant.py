# -*- coding: utf-8 -*-
# File: C:\AI_src\marketing-assistant\ai_marketing_assistant.py

import os
import json
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# ─── Load environment ───────────────────────────────────────────────────────────
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    st.error("🔑 OPENAI_API_KEY not set in environment!")
    st.stop()

# ─── Load Kodey.ai docs ─────────────────────────────────────────────────────────
docs_path = os.path.join(os.getcwd(), "knowledge_base", "kodey_agent_build_docs.txt")
try:
    with open(docs_path, "r", encoding="utf-8") as f:
        kodey_docs = f.read()
except FileNotFoundError:
    kodey_docs = ""
    st.warning(f"⚠️ Could not load Kodey.ai docs at {docs_path}")

# ─── Page config & LLM init ─────────────────────────────────────────────────────
st.set_page_config(page_title="AI Business Optimization Intake", layout="wide")
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, openai_api_key=openai_key)

# ─── Sidebar: Business Profile ─────────────────────────────────────────────────
st.sidebar.header("📋 Business Intake Form")
user_name         = st.sidebar.text_input("Your Name")
business_name     = st.sidebar.text_input("Business Name")
website           = st.sidebar.text_input("Business Website")
industry          = st.sidebar.selectbox(
    "Industry",
    ["Jewelry", "Med Spa", "Real Estate", "Fitness", "Other"]
)
location          = st.sidebar.text_input("Location")
annual_revenue    = st.sidebar.number_input(
    "Annual Revenue (USD)",
    min_value=0, step=1000, value=0, format="%d"
)
employees         = st.sidebar.number_input(
    "Number of Employees",
    min_value=0, step=1, value=0, format="%d"
)

# ─── Main UI ────────────────────────────────────────────────────────────────────
st.title("🧠 AI Solutions Discovery & Optimization Intake")
st.write(
    f"Welcome {user_name} — let's break down your current systems "
    "and find the highest ROI opportunities for automation and AI integration."
)

# Sales & Operations
st.subheader("🧰 Sales & Operations")
sales_process     = st.text_area("Describe your current sales process:")
lead_tools        = st.text_area("What tools do you currently use for leads and appointments?")
has_crm           = st.selectbox("Do you use a CRM?", ["Yes", "No"])
crm_name          = st.text_input("Which CRM do you use (if any)?")
booking_process   = st.text_area("How are appointments currently booked?")
follow_up         = st.text_area("How do you track follow-ups or missed leads?")

# Marketing
st.subheader("📣 Marketing")
channels            = st.multiselect(
    "Active Marketing Channels",
    ["Google Ads", "Meta Ads", "TikTok", "SEO", "Influencer", "Referral", "Events"]
)
lead_routing        = st.text_area("How are leads captured and routed?")
lead_action         = st.text_area("Describe what happens after a lead comes in:")
existing_automations= st.text_area("Any automations currently in place?")

# Engagement & Retention
st.subheader("📞 Engagement & Retention")
sales_cycle         = st.slider("Average Sales Cycle (days)", 1, 180, 30)
follow_up_tactics   = st.text_area("How do you follow up with missed calls, abandoned carts, or no-shows?")
retention           = st.text_area("Any current loyalty, membership, or re-engagement programs?")

# AI & Automation Readiness
st.subheader("🤖 AI & Automation Readiness")
uses_ai             = st.selectbox("Are you using AI currently?", ["Yes", "No"])
ai_tools            = st.text_area("If yes, describe your AI tools or setup.")
manual_areas        = st.multiselect(
    "Where do you spend the most manual time?",
    ["Lead follow-up", "Appointment setting", "Content creation", "Customer questions"]
)
dream_automation    = st.text_area("What would you automate tomorrow if it worked perfectly?")

# Tech Stack
st.subheader("⚙️ Tech Stack")
tools               = st.multiselect(
    "Current Tools in Use",
    ["Calendly", "Shopify", "Squarespace", "Twilio", "Stripe", "Zapier", "Klaviyo", "Mailchimp", "GoHighLevel"]
)
api_access          = st.selectbox("Do you have admin/API access to these tools?", ["Yes", "No", "Not sure"])
comms               = st.selectbox(
    "Preferred customer communication method:",
    ["Text", "Email", "Phone", "DMs", "Website Chat"]
)

# Goals & Timeline
st.subheader("🌟 Goals & Timeline")
goals               = st.text_area("Top 3 revenue goals (next 6 months):")
biggest_problem     = st.text_area("What’s the #1 problem you're trying to solve right now?")
comfort             = st.selectbox(
    "Comfort level with automation/AI:",
    ["Bring on the robots", "Need guidance", "Start simple"]
)
engagement          = st.selectbox(
    "Preferred engagement model:",
    ["Done-For-You", "Hybrid", "DIY with Support"]
)
timeline            = st.selectbox(
    "Implementation timeline:",
    ["<30 days", "30-60 days", "60-90 days", "Flexible"]
)

# HAF/CII Expanders
with st.expander("🔰 Advanced: Hierarchical Agent Framework (HAF)"):
    haf_roles       = st.text_area("List critical roles and their main responsibilities")
    haf_workflows   = st.text_area("Map your key workflows (e.g., Lead → Sale → Delivery)")
    haf_agents      = st.text_area("Which tasks could be delegated to AI agents?")

with st.expander("🧩 Advanced: Cognitive Infrastructure Intake (CII)"):
    memory_needs    = st.text_area("What memory or data history do agents need?")
    agent_tools     = st.text_area("List specific APIs/tools needed for each agent")
    security        = st.text_area("Any compliance or regulatory requirements?")
    latency_critical= st.text_area("Which processes must be real-time vs async?")

# ─── Generate full strategic report & OAB ───────────────────────────────────────
if st.button("🧠 Generate Full Report & Scope"):
    with st.spinner("Generating client report, dev scope & Organizational Agent Blueprint..."):
        try:
            # Assemble structured input
            full_input = {
                "client": {
                    "name":         user_name,
                    "business":     business_name,
                    "website":      website,
                    "industry":     industry,
                    "location":     location,
                    "revenue":      annual_revenue,
                    "employees":    employees
                },
                "operations": {
                    "sales_process": sales_process,
                    "lead_tools":    lead_tools,
                    "crm":           crm_name if has_crm == "Yes" else "None",
                    "booking":       booking_process,
                    "followups":     follow_up
                },
                "marketing": {
                    "channels":      channels,
                    "routing":       lead_routing,
                    "post_lead":     lead_action,
                    "automations":   existing_automations
                },
                "retention": {
                    "sales_cycle":       sales_cycle,
                    "follow_up_tactics": follow_up_tactics,
                    "programs":          retention
                },
                "ai_readiness": {
                    "uses_ai":       uses_ai,
                    "tools":         ai_tools,
                    "manual_areas":  manual_areas,
                    "dream":         dream_automation
                },
                "tech_stack": {
                    "tools":       tools,
                    "api_access":  api_access,
                    "comms":       comms
                },
                "goals_timeline": {
                    "goals":       goals,
                    "problem":     biggest_problem,
                    "comfort":     comfort,
                    "engagement":  engagement,
                    "timeline":    timeline
                },
                "HAF": {
                    "roles":       haf_roles,
                    "workflows":   haf_workflows,
                    "agents":      haf_agents
                },
                "CII": {
                    "memory":      memory_needs,
                    "tools":       agent_tools,
                    "compliance":  security,
                    "latency":     latency_critical
                }
            }
            input_json = json.dumps(full_input, indent=2)

            # System prompt
            system_prompt = (
                "You are a Senior AI Architect & Strategist. Use ONLY the facts in the intake JSON. "
                "Never hallucinate; if data is missing, say 'Insufficient data.' "
                "Produce two sections: Client-Facing and Developer-Facing."
            )

            # Extract top 3 goals safely
            goals_list = [line for line in goals.splitlines() if line.strip()]
            g1 = goals_list[0] if len(goals_list) > 0 else "Insufficient data"
            g2 = goals_list[1] if len(goals_list) > 1 else "Insufficient data"
            g3 = goals_list[2] if len(goals_list) > 2 else "Insufficient data"

            # User prompt
            user_prompt = f"""
INTAKE DATA:
{input_json}

********** CLIENT-FACING REPORT **********

A) Assessment Sales Sheet
- Business Name: {full_input['client']['business']}
- Industry: {full_input['client']['industry']}
- Location: {full_input['client']['location']}
- Revenue: ${full_input['client']['revenue']:,}
- Employees: {full_input['client']['employees']}
- Top 3 Goals:
    1. {g1}
    2. {g2}
    3. {g3}
- #1 Problem: {full_input['goals_timeline']['problem']}

B) Agent Hierarchy Outline
- Supervisor Agent: Oversees all workflows and KPIs.
- Sales Agent: Qualifies leads via chatbot/SMS, triggers follow-up.
- Content Agent: Generates email & social copy.
- Retention Agent: Manages membership & renewal reminders.
- Chatbot Agent: Real-time recommendations & FAQs.

********** DEVELOPER-FACING REPORT **********

A) Technical Assessment & Scope
- Tech Stack: GoHighLevel, Vapi, Twilio, GPT-4o-mini
- Implementation Schedule:
    | Phase | Task                               | Owner       | Effort (hrs) | Timeline (wks) |
    |-------|------------------------------------|-----------|--------------|----------------|
    | 1     | Intake mapping & workflow docs     | Dev Lead    | 12           | 1              |
    | 2     | GHL pipeline & webhook setup       | Engineer    | 16           | 2              |
    | 3     | Vapi agent definitions & tests     | Engineer    | 20           | 3–4            |
    | 4     | Twilio integration & QA            | Engineer    | 8            | 5              |
    | 5     | End-to-end testing & handoff       | Dev Lead    | 6            | 6              |

- Deliverables:
    - GHL pipelines, tags, triggers
    - Vapi agent YAML definitions
    - Twilio SMS/voice flows
    - Deployment scripts & CI checks

B) Organizational Agent Blueprint (OAB)
<Organizational_Agent_Blueprint>
    <description>Use Kodey.ai structure with appropriate prompts and routing.</description>
    <notes>Include Supervisor + 3–5 Executive Agents.</notes>
    <actions>
        <Supervisor_Agent>…routing and prompts…</Supervisor_Agent>
        <Sales_Agent>…</Sales_Agent>
        <Content_Agent>…</Content_Agent>
        <Retention_Agent>…</Retention_Agent>
        <Chatbot_Agent>…</Chatbot_Agent>
    </actions>
</Organizational_Agent_Blueprint>
            """
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = llm(messages)

            st.subheader("📋 Full Strategic Client & Dev Report + OAB")
            st.markdown(response.content)
        except Exception as e:
            st.error(f"An error occurred: {e}")