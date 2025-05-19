import re
import ast
from typing import List
from Scripts.Organizer.models import Skills


def categorize_skills_via_llm(client, skills):
    """
    Sends a list of skills to the LLM for smart categorization (up to 6 title-cased categories),
    and returns a list of Skills(category, skill) objects.
    """
    skill_str = ", ".join(skills)

    system_prompt = (
        "You are a resume assistant that intelligently categorizes technical and soft skills "
        "into fewer than 7 distinct, logical categories. "
        "Each category should be clear, meaningful, and in Title Case (e.g., 'Programming Languages')."
    )

    user_prompt = f"""
Given the following list of skills:

{skill_str}

Categorize them into fewer than 7 meaningful groups with clear category names.
Each category name should be in Title Case (e.g., 'Cloud Platforms', 'Databases', etc.).

Respond in valid Python code using this format:
[
    Skills(category='Programming Languages', skill=['Python', 'C++']),
    Skills(category='Cloud Platforms', skill=['AWS', 'GCP']),
    ...
]
Do not include any extra explanation or text, just the Python list.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=400
    )

    code_output = response.choices[0].message.content.strip()

    # Extract list block from output
    match = re.search(r"(\[.*\])", code_output, re.DOTALL)
    if not match:
        print("❌ Could not extract skill list from LLM output.")
        print("🔎 LLM Output:", code_output)
        return []

    raw_list_code = match.group(1)

    # Convert Skills(...) syntax to dict-like syntax for safe eval
    safe_code = (
        raw_list_code
        .replace("Skills(", "{")
        .replace("category=", "'category': ")
        .replace("skill=", "'skill': ")
        .replace(")", "}")
    )

    try:
        parsed = ast.literal_eval(safe_code)
        return [Skills(category=item['category'], skill=item['skill']) for item in parsed]
    except Exception as e:
        print("❌ Failed to parse skills:", e)
        print("🔎 Raw Safe Code:", safe_code)
        return []