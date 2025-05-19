import os

from Scripts.Extract import yamlparse
from Scripts.Organizer.models import Resume, Education, Project, Experience, Certification, Skills
from Scripts.Doc.doc_developer import render_resume_to_file
from Scripts.Gen.generator import enhance_resume
from dotenv import load_dotenv

import openai


### ---- USER DATA EXTRACTION AND ORGANIZATION ---- ###
# filepath
filepath = os.path.join(os.getcwd(), "Data", "dexmax.yaml")

# data extraction
data = yamlparse.parse_yaml(filepath)

# data organization
education = [Education(**school) for school in data["Education"]["schools"]]
project = [Project(**project) for project in data["Project"]["projects"]]
experience = [Experience(**job) for job in data["Experience"]["jobs"]]
certification = [Certification(**cert) for cert in data["Certification"]["certs"]]
skills = [Skills(**skill) for skill in data["Skills"]["categories"]]
contact = data["Contact"]

# order
education_order = data["Education"]["order"]
experience_order = data["Experience"]["order"]
skills_order = data["Skills"]["order"]
project_order = data["Project"]["order"]
certification_order = data["Certification"]["order"]

resume = Resume(contact, education, experience, skills, project, certification, education_order, experience_order, skills_order, project_order, certification_order)


### ---- KEYWORD EXTRACTION ---- ###
# Load the job description from a file
with open("./Data/JD.txt", "r") as file:
    job_description = file.read()


### ---- ENHANCE RESUME ---- ###
# Load .env file
load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=os.getenv("GROQ_API_BASE")  # Only if using Groq or custom LLM
)


# Enhance the resume
enhanced_resume = enhance_resume(resume, job_description, client)

render_resume_to_file(enhanced_resume)



