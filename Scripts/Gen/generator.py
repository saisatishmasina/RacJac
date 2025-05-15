import re
from Scripts.Organizer.models import Resume, Skills
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc
from typing import Set
import openai
from difflib import SequenceMatcher
import ast


def enhance_resume(resume_obj: Resume, job_description: str, client, nlp) -> Resume:
    MAX_BULLETS = 5

    # Enhance Experience
    for exp in resume_obj.experience:
        if len(exp.summary) >= MAX_BULLETS:
            continue
        context = " ".join(exp.summary)
        new_points = generate_resume_point(job_description, context, client)
        for point in new_points:
            if point and not is_similar_point(point, exp.summary) and len(point.split()) > 3:
                exp.summary.append(point)

    # Enhance Projects
    for proj in resume_obj.projects:
        context = " ".join(proj.summary)
        new_points = generate_resume_point(job_description, context, client)
        for point in new_points:
            if point and not is_similar_point(point, proj.summary) and len(point.split()) > 3:
                proj.summary.append(point)

    # Skills using LLM categorization
    resume_obj.skills = process_skills_with_llm(resume_obj, job_description, nlp, client)

    # Professional Summary
    resume_obj.professional_summary = generate_professional_summary(job_description, resume_obj, client)

    return resume_obj




### ---- RESUME POINT GENERATION ---- ###
def generate_resume_point(job_desc: str, resume_context: str, client) -> str:
    system_prompt = (
        "You are a resume assistant that crafts concise, impactful, and tailored bullet points "
        "for technical resumes. Avoid generic phrases like 'designed and optimized'."
    )

    user_prompt = (
        f"Job Description:\n{job_desc}\n\n"
        f"Resume Context:\n{resume_context}\n\n"
        f"Instructions:\n"
        f"- Generate 1–2 bullet points.\n"
        f"- Each bullet point should be **under 25 words**.\n"
        f"- Avoid phrases like 'designed and optimized', 'leveraging expertise in', or repeating the same structure.\n"
        f"- Focus on *quantifiable results* and *clear accomplishments*.\n"
        f"- Only output the bullet points with no intro, no bullets like '*' or '-'."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )

    raw = response.choices[0].message.content.strip()

    # Extract only lines that look like bullet points (even if model slips)
    bullet_lines = [
        re.sub(r"^[\*\-\d\.\)\s]+", "", line.strip())  # remove bullet-like prefixes
        for line in raw.splitlines()
        if line.strip() and len(line.strip()) < 200  # safeguard
    ]

    return bullet_lines

def is_similar_point(new_point, existing_points, threshold=0.85):
    return any(SequenceMatcher(None, new_point, point).ratio() > threshold for point in existing_points)


##### ---- PROFESSIONAL SUMMARY GENERATION ---- ###

def generate_professional_summary(job_desc: str, resume_data: dict, client) -> str:
    context_parts = []
    for exp in resume_data.experience[:2]:  # Only use top 2 jobs
        context_parts.append(f"{exp.job_title} at {exp.company}: {'; '.join(exp.summary[:2])}")
    for skill_cat in resume_data.skills:
        context_parts.append(f"{skill_cat.category}: {', '.join(skill_cat.skill)}")
    
    resume_context = "\n".join(context_parts)
    
    system_prompt = "You are a helpful resume assistant."
    user_prompt = (
        f"Job Description:\n{job_desc}\n\n"
        f"Resume Highlights:\n{resume_context}\n\n"
        f"Write a professional summary (3-4 lines) that aligns with the job description."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()


### ---- SKILL EXTRACTION ---- ###
def normalize_skill(skill: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\+\.\-\(\)\s]", "", skill.lower().strip())

def process_skills_with_llm(resume_obj: Resume, job_description: str, nlp, client):
    jd_skills = extract_skills_from_text(job_description, nlp)
    resume_skills = extract_resume_skills(resume_obj)

    combined = jd_skills.union(resume_skills)
    normalized = sorted({normalize_skill(skill): skill for skill in combined}.values())

    return categorize_skills_via_llm(client, normalized)

def categorize_skills_via_llm(client, skills):
    """
    Sends the list of skills to the LLM for categorization and returns a list of categorized Skills objects.
    """
    skill_str = ", ".join(skills)

    system_prompt = "You are a professional resume assistant that categorizes skills into standard resume categories."
    user_prompt = f"""
Given the following skills:

{skill_str}

Categorize them into one of the following categories:
- programming_languages
- machine_learning
- cloud
- databases
- tools
- etl
- soft_skills
- other

Respond with valid Python code that instantiates a list of Skills(category, skill) objects.
Each category should have one Skills object, and the skills inside should be a list of strings.

Use this format:
[
    Skills(category='programming_languages', skill=['Python', 'C++']),
    Skills(category='cloud', skill=['AWS', 'GCP']),
    ...
]
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=300
    )

    code_output = response.choices[0].message.content.strip()

    # Extract list block from output
    match = re.search(r"(\[.*\])", code_output, re.DOTALL)
    if not match:
        print("❌ Could not extract skill list from LLM output.")
        print("🔎 LLM Output:", code_output)
        return []

    raw_list_code = match.group(1)

    # Replace Skills(...) with dictionary-like format
    safe_code = (
        raw_list_code
        .replace("Skills(", "{")
        .replace("category=", "'category': ")
        .replace("skill=", "'skill': ")
        .replace(")", "}")
    )

    try:
        # Parse to list of dicts
        parsed = ast.literal_eval(safe_code)
        return [Skills(category=item['category'], skill=item['skill']) for item in parsed]
    except Exception as e:
        print("❌ Failed to parse skills:", e)
        print("🔎 Raw Safe Code:", safe_code)
        return []

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