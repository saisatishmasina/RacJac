import spacy 
from collections import Counter
from spacy.matcher import PhraseMatcher
import re
from typing import Set
from Scripts.Organizer import Resume

nlp = spacy.load("en_core_web_sm")

def extract_keywords(jd_text, top_n=30):
    doc = nlp(jd_text)
    keywords = []

    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 2:
            keywords.append(token.lemma_.lower())

    return [kw for kw, _ in Counter(keywords).most_common(top_n)]

def normalize_skill(skill: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\+\.\-\(\)\s]", "", skill.lower().strip())

def extract_resume_skills(resume_obj: Resume) -> Set[str]:
    return {skill for group in resume_obj.skills for skill in group.skill}

def extract_skills_from_text(text: str, nlp, fallback_keywords: Set[str] = None) -> Set[str]:
    doc = nlp(text)
    if not fallback_keywords:
        return set()

    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    matcher.add("SKILLS", [nlp.make_doc(skill.lower()) for skill in fallback_keywords])

    found = set()
    for _, start, end in matcher(doc):
        found.add(doc[start:end].text.strip())

    return found