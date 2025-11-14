# careerbot/services.py
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GENAI_API_KEY)

def ask_gemini(prompt: str):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text
