# careerbot/services.py
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GENAI_API_KEY)



import json

def generate_cv_assistant_output(pdf_text):
    """
    Generates:
    - professional summary (20 words max)
    - bullet points (max 5)
    - LinkedIn suggestions (25 words max)
    - CV layout (clean formatted text)
    Returns pure JSON (no extra text).
    """

    prompt = f"""
You are an AI CV assistant.
The following is a CV extracted text:

{pdf_text}

Generate a response ONLY in JSON format. Do NOT include markdown or extra explanation.
The JSON MUST follow this exact structure:

{{
  "professional_summary": "string, max 20 words",
  "experience_points": ["max 5 bullet points"],
  "linkedin_suggestions": "string, max 25 words",
  "cv_layout": "formatted clean CV layout as plain text"
}}

Return ONLY valid JSON. No markdown. No explanation.
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        # In case AI still returns markdown ` ```json ` => clean it
        raw = response.text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        return raw  # Now safe to parse with json.loads()
    
    except Exception as e:
        return f"CV Assistant Error: {str(e)}"
