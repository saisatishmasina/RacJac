

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