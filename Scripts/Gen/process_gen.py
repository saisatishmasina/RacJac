from Scripts.Extract.key_extract import extract_skills_via_llm, extract_resume_skills
from Scripts.Gen.skills_gen import categorize_skills_via_llm
from Scripts.Organizer.models import Resume


def process_skills_with_llm(resume_obj: Resume, job_description: str, client):
    jd_skills = extract_skills_via_llm(job_description, client)
    resume_skills = extract_resume_skills(resume_obj)

    combined = set(jd_skills["technical_skills"]).union(resume_skills)

    return categorize_skills_via_llm(client, combined), jd_skills["soft_skills"]