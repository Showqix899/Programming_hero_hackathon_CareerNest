# ai_reasoning.py

import os
from openai import OpenAI
from google import genai
import requests

HF_API_KEY = os.getenv("api_key")
HF_API_URL = os.getenv("base_url")  # e.g., "https://router.huggingface.co/v1"

from .genai_client import model  # Import the initialized Google GenAI model







# HuggingFace/OpenAI client
def get_hf_client():
    return OpenAI(
        base_url=HF_API_URL,
        api_key=HF_API_KEY
    )

# Google GenAI client
def get_genai_client():
    return genai.Client()  # Uses GOOGLE_API_KEY from env




def get_ai_reason(user_skills, user_experience, user_interests, job):
    client = get_hf_client()
    prompt = f"""
    The user has skills: {user_skills}.
    Experience level: {user_experience}.
    Career interests: {user_interests}.
    The job requires skills: {job.required_skills}, experience level: {job.experience_level}, job type: {job.job_type}.

    Write a short explanation for why this job is a good match or what is missing.
    """
    completion = client.chat.completions.create(
        model="google/gemma-2-2b-it:nebius",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message

        
def get_ai_skill_gap(user_skills, job_title, missing_skills):
    """
    Call HuggingFace LLM to explain skill gap and suggest learning resources.
    """
    prompt = f"""
    User Skills: {user_skills}
    Missing Skills: {missing_skills}
    Job Title: {job_title}

    Explain the skill gap in short and suggest learning resources (courses, YouTube, platforms) to fill the gap. Keep it concise.
    """

    try:
        client = get_hf_client()  # make sure you have this helper
        completion = client.chat.completions.create(
            model="google/gemma-2-2b-it:nebius",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message
    except Exception as e:
        return f"Could not generate AI suggestion: {str(e)}"



import google.generativeai as genai
from django.conf import settings

# Configure API key
genai.configure(api_key=settings.GENAI_API_KEY)

# Load model once - FIX: Use the stable, public model name
career_model = genai.GenerativeModel("gemini-2.5-flash") # Changed to gemini-2.5-flash

#text beautifier
def beautify(text: str) -> str:
    return (
        text.replace("\\n", "\n")   # fix newline
            .replace("\\t", "")     # remove tabs
            .replace("*   ", "-")  # bullet cleanup (3 spaces)
            .replace("*  ", "- ")   # bullet cleanup (2 spaces)
            .replace("* ", "- ")    # bullet cleanup (1 space)
            .strip()
    )


def generate_career_roadmap(current_skills, target_role, time_frame="6 months"):
    """
    Generate a personalized career roadmap using Google Gemini.
    """

    prompt = f"""
    You are a professional career mentor.

    User Skills: {', '.join(current_skills)}
    Target Role: {target_role}
    Timeframe: {time_frame}

    Generate a SHORT and BEAUTIFUL career roadmap.

    STRICT FORMAT — DO NOT EXPAND:
    1. **Top 3 Skills to Learn**
    2. **Best 3 Learning Resources**
    3. **Portfolio Projects (max 2)**
    4. **Monthly Milestones (3 bullets)**

    Rules:
    - Keep it VERY SHORT (max 12 lines)
    - Use clean bullet points
    - No long paragraphs
    """

    try:
        response = career_model.generate_content(prompt)
        new_res=beautify(response.text.strip())
        

        return new_res
    except Exception as e:
        return f"Could not generate career roadmap: {str(e)}"
