import streamlit as st
import requests
import json
import os
from datetime import date
import google.generativeai as genai

# ----------- CONFIG ----------- 
st.set_page_config(page_title="AI Marketing Assistant", layout="wide")

# Environment variable fallback (or manually paste your keys here)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBfJz9zcdg9rbSXvreDqvXzErBC4viUw2c")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "93619a3c8d0ec722a369f5e9c5f2c3eabf83dbad95af8ec02c23b36b6f44d25d")

# ----------- USER PROFILE INPUT ----------- 
st.sidebar.header("👤 Your Business Profile")

user_name = st.sidebar.text_input("Your Name")
business_type = st.sidebar.selectbox("Type of Business", ["Food", "Fashion", "Personalized Gifts"])
yearly_income = st.sidebar.number_input("Yearly Income (INR)", step=100)
location = st.sidebar.text_input("Location")

user_profile = {
    "name": user_name,
    "business_type": business_type,
    "yearly_income": yearly_income,
    "location": location
}

# ----------- HEADER ----------- 
st.title("🧠 AI-Powered Marketing Assistant")
st.write(f"👋 Hello {user_profile['name']}, here's your personalized marketing strategy for your *{user_profile['business_type']}* business!")

# ----------- GEMINI STRATEGY SUGGESTIONS ----------- 
def generate_marketing_templates(profile):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp")

    prompt = f"""
You are a helpful digital marketing expert.

The user runs a {profile['business_type']} business based in {profile['location']} 
with an annual revenue of ${profile['yearly_income']}.

Return a marketing strategy suggestion in the following JSON format:

{{
  "marketing_campaign_goals": ["goal1", "goal2", "goal3"],
  "tone_for_posts_and_emails": "tone here",
  "best_post_types": ["type1", "type2", "type3"],
  "posting_frequency_per_week": number
}}

Make sure to consider income and location in your suggestions.
"""

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()

        # Clean JSON block if wrapped in markdown code block
        content = content.split("```json")[-1].split("```")[0].strip() if "```" in content else content

        parsed = json.loads(content)

        return {
            "campaign_goals": parsed.get("marketing_campaign_goals", []),
            "tone": parsed.get("tone_for_posts_and_emails", ""),
            "post_types": parsed.get("best_post_types", []),
            "posting_frequency": parsed.get("posting_frequency_per_week", 0)
        }

    except Exception as e:
        st.error("⚠️ Failed to generate strategy.")
        st.code(str(e))
        return {"error": str(e), "raw": content if 'content' in locals() else ""}

# Fetch strategy suggestions if not already in session state
if "template_data" not in st.session_state:
    st.session_state.template_data = generate_marketing_templates(user_profile)

if st.button("🔁 Refresh Suggestions"):
    st.session_state.template_data = generate_marketing_templates(user_profile)

template_data = st.session_state.template_data

if "error" in template_data:
    st.error(template_data["error"])
    st.code(template_data.get("raw", ""))
    st.stop()

# ----------- STRATEGY DISPLAY ----------- 
st.subheader("📌 Personalized Strategy")
st.markdown("*Campaign Goals:*")
campaign_goals = [str(goal) for goal in template_data.get("campaign_goals", [])]
st.markdown("- " + "\n- ".join(campaign_goals))

st.markdown(f"*Recommended Tone:* {template_data['tone']}")

st.markdown("*Content Types to Focus On:*")
st.markdown("- " + "\n- ".join(template_data["post_types"]))

st.markdown(f"*Posting Frequency:* {template_data['posting_frequency']}")

# ----------- TOGETHER.AI CONTENT CALENDAR ----------- 
def generate_content_calendar(profile, template):
    user_prompt = f"""
Create a 15-day social media content calendar for a {profile['business_type']} brand.
Goals: {', '.join(template['campaign_goals'])}
Tone: {template['tone']}
Post types: {', '.join(template['post_types'])}
Location: {profile['location']}
Income: ${profile['yearly_income']}

Each day should include: Post Idea, Caption, Hashtags.
Format as markdown table.
"""

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are an expert content strategist."},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 10000
    }

    response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

if st.button("📅 Generate 15-Day Content Calendar"):
    with st.spinner("Crafting your content plan..."):
        calendar = generate_content_calendar(user_profile, template_data)
        st.subheader("📆 Your Social Media Calendar")
        st.markdown(calendar)

# ----------- GEMINI EMAIL GENERATOR ----------- 
def generate_email(subject, tone, product):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp")
    prompt = f"Write a promotional email for {product}. Subject: {subject}. Tone: {tone}. Audience: returning customers."
    response = model.generate_content(prompt)
    return response.text

with st.expander("✉ Generate Email Campaign"):
    email_subject = st.text_input("Subject")
    email_product = st.text_input("Product Highlight")
    email_tone = st.selectbox("Tone", ["Friendly", "Exciting", "Elegant", "Professional"])
    if st.button("Generate Email"):
        email_text = generate_email(email_subject, email_tone, email_product)
        st.text_area("Generated Email", email_text, height=300)
