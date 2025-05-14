import spacy 
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def extract_keywords(jd_text, top_n=30):
    doc = nlp(jd_text)
    keywords = []

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 2:
            keywords.append(token.lemma_.lower())

    return [kw for kw, _ in Counter(keywords).most_common(top_n)]
