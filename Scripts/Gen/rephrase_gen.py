from typing import List
import re
from difflib import SequenceMatcher
from Scripts.Organizer import Resume

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



