from jinja2 import Environment, FileSystemLoader
from Scripts.Doc.Utils.helper import render_education, render_experience, render_projects, render_skills, render_certification
from weasyprint import HTML, CSS
import os
from datetime import datetime


def render_resume_to_file(resume,role = "SDE", company="company", output_path="Data/Resumes/resume.pdf"):
    cwd_template = os.path.join(os.getcwd(), "Scripts", "Templates")
    env = Environment(loader=FileSystemLoader(cwd_template))
    template = env.get_template("resume_template.html")

    # Section HTML generation
    sections = []
    order_map = {
        resume.education_order: render_education(resume.education),
        resume.experience_order: render_experience(resume.experience),
        resume.project_order: render_projects(resume.projects),
        resume.skills_order: render_skills(resume.skills),
        resume.certification_order: render_certification(resume.certification)
    }

    for key in sorted(order_map):
        sections.append((key, order_map[key]))

    html_out = template.render(resume=resume, sections=sections)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pdf_bytes = HTML(string=html_out, base_url=cwd_template).write_pdf(
        stylesheets=[CSS(os.path.join(cwd_template, "style.css"))]
    )
    # Generate timestamp-based filename
    timestamp = datetime.now().strftime("%Y-%m-%d")

    # Set your base directory
    base_dir = "/Users/satish/My Documents/Resume Development/Resumes"

    # Format folder name using current date
    folder_name = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(base_dir, folder_name)

    # Check if folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")
    filename_1 = f"Data/Resumes/Resume_{timestamp}_{role}_{company}.pdf"
    filename_2 = os.path.join(folder_path, f"Resume_{timestamp}_{role}_{company}.pdf")
    
    with open(filename_1, "wb") as f:
        f.write(pdf_bytes)
    with open(filename_2, "wb") as f:
        f.write(pdf_bytes)
    print(f"Resume saved to {filename_1} and {filename_2}")
