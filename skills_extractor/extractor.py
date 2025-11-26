
# import spacy
# from .skills_dict import SKILLS, TOOLS, ROLES

# # Load SpaCy English model once
# nlp = spacy.load("en_core_web_sm")


# def extract_keywords(text, keywords_list):
#     extracted = []
#     text_lower = text.lower()
#     for keyword in keywords_list:
#         if keyword.lower() in text_lower:
#             extracted.append(keyword)
#     return extracted


# def extract_entities(text):
#     """
#     Extracts nouns, noun phrases, and basic entities using spaCy (local NLP).
#     """
#     doc = nlp(text)

#     entities = set()

#     # Noun phrases (e.g. "machine learning engineer", "python developer")
#     for chunk in doc.noun_chunks:
#         entities.add(chunk.text)

#     # Named entities (ORG, PERSON, ROLES, TECHNOLOGIES)
#     for ent in doc.ents:
#         entities.add(ent.text)

#     return list(entities)


# def extract_all(text):
#     """
#     SAME NAME & SAME PURPOSE as before.
#     Replaces AI call with LOCAL NLP.
#     """

#     # Use spaCy instead of AI output
#     nlp_entities = extract_entities(text)

#     # Return same structure, except ai_output removed
#     return {
#         "skills": extract_keywords(text, SKILLS),
#         "tools": extract_keywords(text, TOOLS),
#         "roles": extract_keywords(text, ROLES),
#         "nlp_entities": nlp_entities,  # new local NLP insights
#     }
import spacy
import re
from collections import Counter
from .skills_dict import SKILLS, TOOLS, ROLES

nlp = spacy.load("en_core_web_sm")


def clean_text(text):
    """ Remove useless symbols & normalize spaces """
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()     # extra spaces
    return text.lower()


def extract_keywords_with_count(text, keywords_list):
    """
    Finds keywords AND how many times they appear → confidence score
    """
    text_lower = text.lower()
    result = {}
    for keyword in keywords_list:
        count = text_lower.count(keyword.lower())
        if count > 0:
            result[keyword] = count  # e.g. {'python': 3}
    return result


def extract_entities(text):
    """
    Extracts noun phrases & entities using SpaCy.
    """
    doc = nlp(text)
    entities = set()

    # More powerful noun extraction
    for chunk in doc.noun_chunks:
        if len(chunk.text) > 2:  # ignore tiny words
            entities.add(chunk.text)

    # Named entities (ORGANIZATIONS, PERSON, LOCATIONS)
    for ent in doc.ents:
        entities.add(ent.text)

    return list(entities)


def extract_missing_keywords(extracted, source):
    """ Return what skills are MISSING (job matching possible!) """
    return list(set(source) - set(extracted.keys()))


def extract_all(text):
    """
    MAIN FUNCTION — Final improved engine
    """

    # STEP 1) CLEAN TEXT
    text = clean_text(text)

    # STEP 2) SKILL / TOOL / ROLE MATCHING WITH FREQUENCY
    skills_found = extract_keywords_with_count(text, SKILLS)
    tools_found = extract_keywords_with_count(text, TOOLS)
    roles_found = extract_keywords_with_count(text, ROLES)

    # STEP 3) NLP ENTITIES
    nlp_entities = extract_entities(text)

    # STEP 4) MISSING MATCHES
    missing_skills = extract_missing_keywords(skills_found, SKILLS)
    missing_tools = extract_missing_keywords(tools_found, TOOLS)
    missing_roles = extract_missing_keywords(roles_found, ROLES)

    return {
        "skills_found": skills_found,
        "tools_found": tools_found,
        "roles_found": roles_found,
        "nlp_entities": nlp_entities,

        # NEW EXTRA FEATURES:
        "missing_skills": missing_skills,
        "missing_tools": missing_tools,
        "missing_roles": missing_roles,

        # Confidence Score (sum of occurrences)
        "confidence_score": sum(skills_found.values()) +
                            sum(tools_found.values()) +
                            sum(roles_found.values())
    }
