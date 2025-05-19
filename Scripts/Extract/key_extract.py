from typing import Set
import re
from Scripts.Organizer.models import Resume

def extract_skills_via_llm(jd_text: str, client):
    system_prompt = (
        "You are an expert resume assistant. Given a job description, extract two clearly separated lists:\n"
        "- Technical Skills (e.g., programming languages, tools, frameworks, platforms, databases, etc.)\n"
        "- Soft Skills (e.g., communication, leadership, adaptability, teamwork, etc.)\n"
        "Do not hallucinate; only include what is clearly mentioned or strongly implied."
    )

    user_prompt = f"""
Job Description:
\"\"\"
{jd_text}
\"\"\"

Output Format (Python-style dictionary):

{{
    "technical_skills": [...],
    "soft_skills": [...]
}}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=400
    )

    output = response.choices[0].message.content.strip()

    def extract_list_by_key(text, key):
        pattern = rf'"{key}"\s*:\s*\[(.*?)\]'
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            return set()
        raw_list = match.group(1)
        # Extract individual items, stripping quotes and whitespace
        return {
            item.strip().strip('"').strip("'")
            for item in re.findall(r'["\'](.*?)["\']', raw_list)
        }

    technical_skills = extract_list_by_key(output, "technical_skills")
    soft_skills = extract_list_by_key(output, "soft_skills")

    return {
        "technical_skills": technical_skills,
        "soft_skills": soft_skills
    }

def extract_resume_skills(resume_obj: Resume) -> Set[str]:
    return {skill for group in resume_obj.skills for skill in group.skill}