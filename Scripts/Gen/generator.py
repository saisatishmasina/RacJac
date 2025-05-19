from Scripts.Organizer.models import Resume
from difflib import SequenceMatcher
from Scripts.Gen.rephrase_gen import is_similar_point
from Scripts.Gen.process_gen import process_skills_with_llm
from Scripts.Gen.summary_gen import generate_professional_summary
from Scripts.Gen.rephrase_gen import generate_resume_summary_points

def enhance_resume(resume_obj: Resume, job_description: str, client) -> Resume:
    MAX_BULLETS = 5

    # Enhance Experience
    for exp in resume_obj.experience:
        if len(exp.summary) >= MAX_BULLETS:
            continue
        context = " ".join(exp.summary)
        new_points = generate_resume_summary_points(job_description, context, client)
        for point in new_points:
            if point and not is_similar_point(point, exp.summary) and len(point.split()) > 3:
                exp.summary.append(point)

    # Enhance Projects
    for proj in resume_obj.projects:
        context = " ".join(proj.summary)
        new_points = generate_resume_summary_points(job_description, context, client)
        for point in new_points:
            if point and not is_similar_point(point, proj.summary) and len(point.split()) > 3:
                proj.summary.append(point)

    # Skills using LLM categorization
    resume_obj.skills, soft_skills = process_skills_with_llm(resume_obj, job_description, client)

    # Professional Summary
    resume_obj.professional_summary = generate_professional_summary(job_description, resume_obj, client)

    return resume_obj



