import json
from graph import run_pipeline

# Multiple industry variations
test_inputs = [
    {
        "ClientProfile": {
            "name": "Sasha Stone", "business": "Luxe Lounge Med Spa",
            "website": "https://luxelounge.com", "industry": "Med Spa",
            "location": "Scottsdale, AZ", "revenue": 420000, "employees": 6
        },
        "SalesOps": {
            "sales_process": "Initial consult → service package → follow-up membership",
            "lead_tools": "Jotform, Google Ads leads",
            "crm": "GoHighLevel", "booking": "Through GHL calendar",
            "followups": "Daily call list pulled by receptionist"
        },
        "Marketing": {
            "channels": ["Meta Ads", "Google Ads"], "routing": "Zapier → CRM",
            "post_lead": "Receptionist calls all qualified leads",
            "automations": "Birthday emails, post-treatment check-in messages"
        },
        "Retention": {
            "sales_cycle": 5, "follow_up_tactics": "Text + email combo after 2 days",
            "programs": "Monthly facial membership, loyalty points"
        },
        "AIReadiness": {
            "uses_ai": "No", "tools": "",
            "manual_areas": ["Follow-up", "Appointment setting"],
            "dream": "Automated consult follow-up and rebooking"
        },
        "TechStack": {
            "tools": ["Zapier", "GoHighLevel", "Twilio"], "api_access": "Yes", "comms": "Text"
        },
        "GoalsTimeline": {
            "goals": "1. Increase monthly memberships 2. Cut lead response time 3. Reduce cancellations",
            "problem": "No-shows and follow-up delays",
            "comfort": "Start simple", "engagement": "Done-For-You", "timeline": "30-60 days"
        },
        "HAF": {
            "CriticalRoles": "Receptionist, Manager",
            "RoleResponsibilities": "Booking and follow-up handled manually",
            "KeyWorkflows": "Lead → Call → Consult → Service → Follow-up",
            "AIEligibleTasks": "No-show reminders, post-consult follow-up",
            "HandoffPoints": "Booking to service",
            "DecisionPoints": "Lead quality threshold for call priority"
        },
        "CII": {
            "DataSources": "GoHighLevel, Twilio",
            "MemoryRequirements": "Consultation notes, treatment history",
            "ToolsByFunction": "GHL for leads and SMS",
            "APIReadiness": "Yes", "ComplianceFlags": "HIPAA-sensitive notes",
            "Latency": {"Realtime": "Inbound booking", "Async": "Marketing email flows"}
        },
        "ReferenceDocs": ""
    },
    {
        "ClientProfile": {
            "name": "Marcus Blake", "business": "Skyline Realty Group",
            "website": "https://skyrealtygroup.com", "industry": "Real Estate",
            "location": "Tampa, FL", "revenue": 890000, "employees": 14
        },
        "SalesOps": {
            "sales_process": "Agent shows → CRM logs → offer → closing",
            "lead_tools": "Zillow, Facebook Lead Ads",
            "crm": "Follow Up Boss", "booking": "Calendly for showing requests",
            "followups": "Agents responsible via call + SMS"
        },
        "Marketing": {
            "channels": ["SEO", "Facebook Ads", "Referral"], "routing": "Zapier → CRM",
            "post_lead": "Assigned to agent by rotation",
            "automations": "Just listed drip campaigns"
        },
        "Retention": {
            "sales_cycle": 21, "follow_up_tactics": "3-day follow-up and email campaign",
            "programs": "Homeowner referrals, closing gift incentive"
        },
        "AIReadiness": {
            "uses_ai": "Yes", "tools": "ChatGPT for blog posts",
            "manual_areas": ["Follow-up", "Appointment setting"],
            "dream": "Auto-assign leads and route them to agents"
        },
        "TechStack": {
            "tools": ["Zapier", "Calendly", "Follow Up Boss"], "api_access": "Yes", "comms": "Phone"
        },
        "GoalsTimeline": {
            "goals": "1. Cut response times 2. Improve conversion 3. Boost referral reuse",
            "problem": "Agents forget to follow-up fast enough",
            "comfort": "Need guidance", "engagement": "Hybrid", "timeline": "60-90 days"
        },
        "HAF": {
            "CriticalRoles": "Lead Manager, 10 field agents",
            "RoleResponsibilities": "Distribute, follow-up, close",
            "KeyWorkflows": "Lead → Assign → Call → Schedule",
            "AIEligibleTasks": "Auto-assign, SMS draft + send",
            "HandoffPoints": "Lead manager → Agent",
            "DecisionPoints": "Lead volume triggers reassignment"
        },
        "CII": {
            "DataSources": "Follow Up Boss, Gmail, Google Sheets",
            "MemoryRequirements": "Agent interactions, stage in deal flow",
            "ToolsByFunction": "FUB for CRM, Sheets for KPIs",
            "APIReadiness": "Yes", "ComplianceFlags": "None",
            "Latency": {"Realtime": "Inbound leads", "Async": "Reporting and KPIs"}
        },
        "ReferenceDocs": ""
    }
]

# Execute
for i, biz in enumerate(test_inputs):
    print(f"\n====== Business #{i+1} — {biz['ClientProfile']['business']} ======")
    try:
        out = run_pipeline(biz)
        print("\n📄 Client-Facing Report:\n")
        print(out["client_report"])
        print("\n📋 Dev-Facing Blueprint:\n")
        print(out["dev_report"])
    except Exception as e:
        print(f"❌ Error during test {i+1}: {e}")
