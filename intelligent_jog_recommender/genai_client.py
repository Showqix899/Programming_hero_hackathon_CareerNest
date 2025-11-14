import google.generativeai as genai
from django.conf import settings

if not settings.GENAI_API_KEY:
    raise ValueError("GENAI_API_KEY missing from .env")

genai.configure(api_key=settings.GENAI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
