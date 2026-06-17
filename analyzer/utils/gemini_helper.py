import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_resume(resume_text, target_role):
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are an ATS expert.

Analyze the following resume for the target role.

Target Role:
{target_role}

Resume:
{resume_text}

Reply ONLY with valid JSON in this exact format:

{{
    "ats_score": 0,
    "matched_keywords": [],
    "missing_keywords": [],
    "suggestions": ""
}}
"""

    response = model.generate_content(prompt)

    raw = response.text.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]

        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())