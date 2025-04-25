from jinja2 import Environment, FileSystemLoader
from Scripts.Doc.Utils.helper import render_education, render_experience, render_projects, render_skills, render_certification
from weasyprint import HTML, CSS
import os


def render_resume_to_file(resume, output_path="output/tailored_resume.txt"):
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

    with open("output/resume.pdf", "wb") as f:
        f.write(pdf_bytes)
