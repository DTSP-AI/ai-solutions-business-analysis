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

# ─── (Optional) Load Kodey.ai docs ──────────────────────────────────────────────
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
user_name      = st.sidebar.text_input("Your Name")
business_name  = st.sidebar.text_input("Business Name")
website        = st.sidebar.text_input("Business Website")
industry       = st.sidebar.selectbox("Industry", ["Jewelry", "Med Spa", "Real Estate", "Fitness", "Other"])
location       = st.sidebar.text_input("Location")
annual_revenue = st.sidebar.number_input("Annual Revenue (USD)", min_value=0, step=1000, value=0, format="%d")
employees      = st.sidebar.number_input("Number of Employees", min_value=0, step=1, value=0, format="%d")

# ─── Main UI ────────────────────────────────────────────────────────────────────
st.title("🧠 AI Solutions Discovery & Optimization Intake")
st.write(
    f"Welcome {user_name} — let's break down your current systems "
    "and find the highest ROI opportunities for automation and AI integration."
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
channels             = st.multiselect("Active Marketing Channels", ["Google Ads","Meta Ads","TikTok","SEO","Influencer","Referral","Events"])
lead_routing         = st.text_area("How are leads captured and routed?")
lead_action          = st.text_area("Describe what happens after a lead comes in:")
existing_automations = st.text_area("Any automations currently in place?")

# Engagement & Retention
st.subheader("📞 Engagement & Retention")
sales_cycle        = st.slider("Average Sales Cycle (days)", 1, 180, 30)
follow_up_tactics  = st.text_area("How do you follow up with missed calls, abandoned carts, or no-shows?")
retention          = st.text_area("Any current loyalty, membership, or re-engagement programs?")

# AI & Automation Readiness
st.subheader("🤖 AI & Automation Readiness")
uses_ai          = st.selectbox("Are you using AI currently?", ["Yes", "No"])
ai_tools         = st.text_area("If yes, describe your AI tools or setup.")
manual_areas     = st.multiselect("Where do you spend the most manual time?", ["Lead follow-up","Appointment setting","Content creation","Customer questions"])
dream_automation = st.text_area("What would you automate tomorrow if it worked perfectly?")

# Tech Stack
st.subheader("⚙️ Tech Stack")
tools      = st.multiselect("Current Tools in Use", ["Calendly","Shopify","Squarespace","Twilio","Stripe","Zapier","Klaviyo","Mailchimp","GoHighLevel"])
api_access = st.selectbox("Do you have admin/API access to these tools?", ["Yes","No","Not sure"])
comms      = st.selectbox("Preferred customer communication method:", ["Text","Email","Phone","DMs","Website Chat"])

# Goals & Timeline
st.subheader("🌟 Goals & Timeline")
goals           = st.text_area("Top 3 revenue goals (next 6 months):")
biggest_problem = st.text_area("What’s the #1 problem you're trying to solve right now?")
comfort         = st.selectbox("Comfort level with automation/AI:", ["Bring on the robots","Need guidance","Start simple"])
engagement      = st.selectbox("Preferred engagement model:", ["Done-For-You","Hybrid","DIY with Support"])
timeline        = st.selectbox("Implementation timeline:", ["<30 days","30-60 days","60-90 days","Flexible"])

# HAF/CII Expanders
with st.expander("🔰 Advanced: Hierarchical Agent Framework (HAF)"):
    haf_roles     = st.text_area("List critical roles and their main responsibilities")
    haf_workflows = st.text_area("Map your key workflows (e.g., Lead → Sale → Delivery)")
    haf_agents    = st.text_area("Which tasks could be delegated to AI agents?")

with st.expander("🧩 Advanced: Cognitive Infrastructure Intake (CII)"):
    memory_needs    = st.text_area("What memory or data history do agents need?")
    agent_tools     = st.text_area("List specific APIs/tools needed for each agent")
    security        = st.text_area("Any compliance or regulatory requirements?")
    latency_critical= st.text_area("Which processes must be real-time vs async?")

# ─── Two-Agent Flow: Structured Summary → Full OAB ──────────────────────────────
if st.button("🧠 Generate Full Report & Scope"):
    with st.spinner("Building structured summary, then full OAB..."):

        # Assemble raw intake dict
        full_input = {
            "client": {
                "name":      user_name,
                "business":  business_name,
                "website":   website,
                "industry":  industry,
                "location":  location,
                "revenue":   annual_revenue,
                "employees": employees
            },
            "operations": {
                "sales_process": sales_process,
                "lead_tools":    lead_tools,
                "crm":           crm_name if has_crm == "Yes" else "None",
                "booking":       booking_process,
                "followups":     follow_up
            },
            "marketing": {
                "channels":    channels,
                "routing":     lead_routing,
                "post_lead":   lead_action,
                "automations": existing_automations
            },
            "retention": {
                "sales_cycle":       sales_cycle,
                "follow_up_tactics": follow_up_tactics,
                "programs":          retention
            },
            "ai_readiness": {
                "uses_ai":      uses_ai,
                "tools":        ai_tools,
                "manual_areas": manual_areas,
                "dream":        dream_automation
            },
            "tech_stack": {
                "tools":      tools,
                "api_access": api_access,
                "comms":      comms
            },
            "goals_timeline": {
                "goals":      goals,
                "problem":    biggest_problem,
                "comfort":    comfort,
                "engagement": engagement,
                "timeline":   timeline
            },
            "HAF": {
                "roles":     haf_roles,
                "workflows": haf_workflows,
                "agents":    haf_agents
            },
            "CII": {
                "memory":    memory_needs,
                "tools":     agent_tools,
                "compliance":security,
                "latency":   latency_critical
            }
        }
        raw_json = json.dumps(full_input, indent=2)

        # ── Agent 1: Structured Intake Summary ────────────────────────────────
        summary_system = SystemMessage(
            content=(
                "You are an Intake Summarizer. Convert the raw intake JSON into a clean, "
                "validated summary JSON with top-level keys: ClientProfile, SalesOps, "
                "Marketing, Retention, AIReadiness, TechStack, GoalsTimeline, HAF, CII. "
                "Output JSON only."
            )
        )
        summary_user = HumanMessage(content=f"INTAKE_JSON:\n{raw_json}")
        summary_resp = llm([summary_system, summary_user])
        structured_summary = summary_resp.content

        # (Optional) Show the normalized summary
        st.subheader("📝 Structured Intake Summary")
        st.code(structured_summary, language="json")

        # ── Agent 2: Full Client- & Dev-Facing OAB ────────────────────────────
        oab_system = SystemMessage(
            content=(
                "You are the Organizational Agent Blueprint Architect. "
                "Take the intake summary JSON and produce two deliverables:\n"
                "1) A Client-Facing Report in markdown (Assessment + Proposed Agent Org Structure).\n"
                "2) A Developer-Facing OAB in XML, including Supervisor Prompt, <agents>, "
                "<routing_logic>, and each agent’s full prompt (description, notes, capabilities, actions, error_handling).\n"
                "Do NOT hallucinate—if any field is missing, output “Insufficient data.”"
            )
        )
        oab_user = HumanMessage(content=f"INTAKE_SUMMARY_JSON:\n{structured_summary}")
        oab_resp = llm([oab_system, oab_user])

        # ── Render Final Output ────────────────────────────────────────────────
        st.subheader("📋 Full Strategic Client & Dev Report + OAB")
        st.markdown(oab_resp.content)
