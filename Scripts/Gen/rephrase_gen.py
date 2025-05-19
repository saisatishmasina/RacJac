from typing import List
import re
from difflib import SequenceMatcher


def generate_resume_summary_points(job_desc: str, resume_context: str, client, context_type="experience") -> list[str]:
    prompt_templates = {
        "summary": (
            "You are a resume assistant optimizing professional summaries to match job descriptions. "
            "Rewrite into 2–4 crisp, tailored bullet points under 25 words. Use job keywords, avoid fluff."
        ),
        "experience": (
            "You are a resume assistant improving job experience bullet points to match job descriptions. "
            "Rewrite the input into 3–6 concise bullets (max 35 words each) focusing on impact, metrics, and technologies. "
            "Use relevant keywords naturally. Avoid generic phrases like 'responsible for'."
        ),
        "project": (
            "You are a resume assistant improving project descriptions to better match job descriptions. "
            "Rewrite the input into 3–6 impactful bullet points (max 35 words each) emphasizing outcomes, tech used, and innovation. "
            "Match the job's keywords naturally."
        )
    }

    system_prompt = prompt_templates.get(context_type, prompt_templates["experience"])

    user_prompt = (
        f"Job Description:\n{job_desc}\n\n"
        f"Resume Context ({context_type}):\n{resume_context}\n\n"
        f"Instructions:\n"
        f"- Rewrite into 3–6 bullet points.\n"
        f"- Each bullet should be under 35 words.\n"
        f"- Use keywords from the job description naturally.\n"
        f"- Highlight measurable results or technologies.\n"
        f"- No generic phrases like 'responsible for'.\n"
        f"- Output only the bullet points.\n"
        f"- No bullet symbols like '-', '*', or numbering."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6,
        max_tokens=400
    )

    raw = response.choices[0].message.content.strip()

    bullet_lines = [
        re.sub(r"^[\*\-\d\.\)\s]+", "", line.strip())
        for line in raw.splitlines()
        if line.strip() and len(line.strip()) < 200
    ]

    return bullet_lines

def is_similar_point(new_point, existing_points, threshold=0.85):
    return any(SequenceMatcher(None, new_point, point).ratio() > threshold for point in existing_points)



