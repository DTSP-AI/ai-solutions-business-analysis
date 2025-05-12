import json
from graph import run_pipeline

# Single test input
test_business = {
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
}

# Execute test
print(f"\n====== Testing: {test_business['ClientProfile']['business']} ======")
try:
    out = run_pipeline(test_business)
    print("\n📄 Client-Facing Report:\n")
    print(out["client_report"])
    print("\n📋 Dev-Facing Blueprint:\n")
    print(out["dev_report"])
except Exception as e:
    print(f"❌ Error: {e}")
