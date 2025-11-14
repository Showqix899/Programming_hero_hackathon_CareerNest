# careerbot/services.py
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GENAI_API_KEY)



def generate_cv_assistant_output(pdf_text):
    """
    Takes extracted CV text and generates:
    - Professional summary
    - Bullet points
    - LinkedIn improvement suggestions
    """

    prompt = f"""
    The following text is extracted from a user's CV:

    {pdf_text}

    Based on this CV:

    1. Generate a strong, concise professional summary. maximum 20 words
    2. Rewrite the user's experience into powerful, ATS-friendly bullet points. maximum 5 points
    3. Suggest practical ways to improve the user's LinkedIn profile and portfolio. 25 words
    4. Keep formatting clean and readable.
    5. also generate a clean CV layout for the User
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"CV Assistant Error: {str(e)}"