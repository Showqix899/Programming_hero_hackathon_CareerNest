import re

def fix_broken_words(text):
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Merge words like: F eni → Feni  |  S aiful → Saiful
    text = re.sub(r'\b([A-Za-z])\s+([a-z]+)\b', r'\1\2', text)

    return text
