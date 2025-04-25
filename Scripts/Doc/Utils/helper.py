def render_contact(contact):
    addr = contact["address"]
    return f"""
    <h2>Contact</h2>
    <hr>
    <p><strong>Name:</strong> {contact['name']}</p>
    <p><strong>Email:</strong> {contact['email']}</p>
    <p><strong>Phone:</strong> {contact['phone_number']}</p>
    <p><strong>Address:</strong> {addr['street']}, {addr['city']}, {addr['state']} - {addr['zip']}</p>
    """

def render_education(schools):
    result = "<h2>EDUCATION</h2>"
    result += "<hr>"
    for school in schools:
        result += f"""
        <p><strong>{school.degree} in {school.major}</strong> — {school.name}</p>
        <p>GPA: {school.gpa}</p>
        <p>Relevant Courses: {','.join(f'{course}' for course in school.related_courses)}
        </p>
        """
    return result

def render_experience(jobs):
    result = "<h2>EXPERIENCE</h2>"
    result += "<hr>"
    for job in jobs:
        result += f"""
        <div class="job-header">
            <span class="job-title">{job.job_title} at {job.company}</span>
            <span class="job-dates">{job.duration}</span>
        </div>
        <p>Skills Used: {', '.join(job.skills_used)}</p>
        <ul>
        {''.join(f'<li>{line}</li>' for line in job.summary)}
        </ul>
        """
    return result

def render_projects(projects):
    result = "<h2>PROJECTS</h2>"
    result += "<hr>"
    for proj in projects:
        result += f"""
        <p><strong>{proj.project_name}</strong> ({', '.join(proj.skills_used)})</p>
        <ul>
        {''.join(f'<li>{line}</li>' for line in proj.summary)}
        </ul>
        """
    return result

def render_skills(skills):
    result = "<h2>TECHNICAL SKILLS</h2>"
    result += "<hr>"
    for cat in skills:
        result += f"<p><strong>{cat.category}:</strong> {', '.join(cat.skill)}</p>"
    return result

def render_certification(certs):
    result = "<h2>CERTIFICATIONS</h2>"
    result += "<hr>"
    for cert in certs:
        result += f"""
        <p>
        <a href="{cert.link}">{cert.name}</a>
        </p>
        """
    return result