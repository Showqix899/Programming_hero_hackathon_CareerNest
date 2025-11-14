
import spacy
from .skills_dict import SKILLS, TOOLS, ROLES

# Load SpaCy English model once
nlp = spacy.load("en_core_web_sm")


def extract_keywords(text, keywords_list):
    extracted = []
    text_lower = text.lower()
    for keyword in keywords_list:
        if keyword.lower() in text_lower:
            extracted.append(keyword)
    return extracted


def extract_entities(text):
    """
    Extracts nouns, noun phrases, and basic entities using spaCy (local NLP).
    """
    doc = nlp(text)

    entities = set()

    # Noun phrases (e.g. "machine learning engineer", "python developer")
    for chunk in doc.noun_chunks:
        entities.add(chunk.text)

    # Named entities (ORG, PERSON, ROLES, TECHNOLOGIES)
    for ent in doc.ents:
        entities.add(ent.text)

    return list(entities)


def extract_all(text):
    """
    SAME NAME & SAME PURPOSE as before.
    Replaces AI call with LOCAL NLP.
    """

    # Use spaCy instead of AI output
    nlp_entities = extract_entities(text)

    # Return same structure, except ai_output removed
    return {
        "skills": extract_keywords(text, SKILLS),
        "tools": extract_keywords(text, TOOLS),
        "roles": extract_keywords(text, ROLES),
        "nlp_entities": nlp_entities,  # new local NLP insights
    }
