import os

from Scripts.Extract import yamlparse
from Scripts.Organizer.models import Resume, Education, Project, Experience, Certification, Skills
from Scripts.Doc.doc_developer import render_resume_to_file

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

render_resume_to_file(resume)



