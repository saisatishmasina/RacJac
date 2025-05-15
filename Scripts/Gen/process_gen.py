from Scripts.Extract.key_extract import extract_skills_from_text, extract_resume_skills, normalize_skill
from Scripts.Gen.skills_gen import categorize_skills_via_llm
from Scripts.Organizer import Resume


def process_skills_with_llm(resume_obj: Resume, job_description: str, nlp, client):
    jd_skills = extract_skills_from_text(job_description, nlp)
    resume_skills = extract_resume_skills(resume_obj)

    combined = jd_skills.union(resume_skills)
    normalized = sorted({normalize_skill(skill): skill for skill in combined}.values())

    return categorize_skills_via_llm(client, normalized)