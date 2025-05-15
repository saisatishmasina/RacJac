import re
import ast
from typing import List
from Scripts.Organizer import Skills


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

