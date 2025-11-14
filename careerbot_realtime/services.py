import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GENAI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"

def ask_gemini(prompt: str, temperature: float = 0.2):
    model = genai.get_model(MODEL_NAME)
    resp = model.generate(
    input=prompt,
    temperature=temperature,
    )
    # The SDK returns structured object; pick text safely
    text = ''
    if hasattr(resp, 'candidates') and len(resp.candidates) > 0:
        text = resp.candidates[0].content[0].text
    elif hasattr(resp, 'output'):
        text = getattr(resp.output, 'text', '')
    return text