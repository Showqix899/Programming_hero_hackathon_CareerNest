# careerbot/prompts.py


def build_career_prompt(user_profile, question):
    profile_summary = f"Skills: {user_profile.skills or ''}\nExperience: {user_profile.experience or ''}\nInterests: {user_profile.career_interests or ''}\n"
    cv = user_profile.cv_text or user_profile.pdf_text or ''
    prompt = f"""
    You are CareerBot, an expert career mentor. Use the user's profile to answer concisely and actionably.


    User Profile:\n{profile_summary}\nCV Summary:\n{cv}\n
    User question: {question}\n
    Provide:
    1) Short recommended roles (2-5)
    2) Skills to learn (3-6) with resources
    3) Concrete next steps for the next 30/90 days
    Format your output as JSON with keys: roles, skills_to_learn, next_steps, resume_feedback
    """
    return prompt