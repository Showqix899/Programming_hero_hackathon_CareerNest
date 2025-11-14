from .skills_dict import SKILLS, TOOLS, ROLES

def extract_keywords(text, keywords_list):
    extracted = []

    text_lower = text.lower()

    for keyword in keywords_list:
        if keyword.lower() in text_lower:
            extracted.append(keyword)

    return extracted


def extract_all(text):

    prompt = "extract skills tools and roles accordint to the text and give me as python dictionary"



    return {
        "skills": extract_keywords(text, SKILLS),
        "tools": extract_keywords(text, TOOLS),
        "roles": extract_keywords(text, ROLES)
    }
