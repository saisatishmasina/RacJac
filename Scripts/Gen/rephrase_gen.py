from typing import List
import re
from difflib import SequenceMatcher


def generate_resume_summary_points(job_desc: str, resume_context: str, client, context_type="experience") -> list[str]:
    prompt_templates = {
        "summary": (
        "You are a resume assistant optimizing professional summaries for ATS and recruiters. "
        "Output exactly 3–4 crisp bullet points (max 20 words each). "
        "Each bullet must: (1) use 1–2 keywords from the job description, "
        "(2) highlight measurable achievements, "
        "(3) use different types of quantification (%, time saved, reliability, cost, adoption, scale). "
        "No duplicate metrics."
        ),
        "experience": (
            "You are a resume assistant rewriting job experience bullets for ATS and recruiters. "
            "Output exactly 4–6 concise, unique bullets (max 25 words each). Rules: "
            "• Start each bullet with a strong action verb. "
            "• Use one unique technology/tool per bullet. "
            "• Rotate metrics across bullets: "
            "(a) % improvement, (b) time saved, (c) reliability/uptime, "
            "(d) cost savings, (e) scale/volume handled, (f) adoption/usage growth. "
            "• Each bullet must use a different metric type. "
            "• Do not exceed 6 bullets per job."
        ),
        "project": (
            "You are a resume assistant rewriting project descriptions for ATS and recruiters. "
            "Output exactly 3–4 concise bullets (max 25 words each). Rules: "
            "• Start with a strong action verb. "
            "• Each bullet must highlight at least one technology. "
            "• Rotate quantification across bullets: "
            "(a) % improvement, (b) hours or days saved, (c) adoption rate, "
            "(d) reliability/uptime, (e) cost savings. "
            "• No two bullets may use the same metric type. "
            "• Do not exceed 4 bullets per project."
        )
    }

    system_prompt = prompt_templates.get(context_type, prompt_templates["experience"])
    
    if context_type == "summary":
        bullet_range = "3–4 bullet points"
    elif context_type == "project":
        bullet_range = "3–4 bullet points"
    else:  # experience
        bullet_range = "4–6 bullet points"

    user_prompt = (
        f"Job Description:\n{job_desc}\n\n"
        f"Resume Context ({context_type}):\n{resume_context}\n\n"
        f"Instructions:\n"
        f"- Rewrite into {bullet_range} following the system rules above.\n"
        f"- Each bullet should be under 25 words (35 words max for experience if needed).\n"
        f"- Use keywords from the job description naturally.\n"
        f"- Highlight measurable results or technologies.\n"
        f"- Rotate quantification styles (%, time saved, reliability, cost, scale, adoption) with no duplicates.\n"
        f"- No generic phrases like 'responsible for'.\n"
        f"- Output only the bullet points.\n"
        f"- Do not use bullet symbols like '-', '*', or numbering."
    )
    

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
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



