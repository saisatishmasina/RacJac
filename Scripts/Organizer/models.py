class Resume:

    def __init__(self, contact, education, experience, skills, project, certification, education_order, experience_order, skills_order, project_order, certification_order):
        # data objects
        self.contact = contact
        self.education = education
        self.experience = experience
        self.skills = skills
        self.projects = project
        self.certification = certification

        # order variables
        self.education_order = education_order
        self.experience_order = experience_order
        self.skills_order = skills_order
        self.project_order = project_order
        self.certification_order = certification_order
        
        #generated variables
        self.professional_summary = ""

    def display(self):
        print("-"*40 + "Resume" + "-"*40)
        print(f"Professional Summary:\n{self.professional_summary}")
        self.display_contact()
        for _, display_func in self.display_order_by_section():
            display_func()
        print("-"*40 + "End of Resume" + "-"*40)
    
    # display functions
    def display_order_by_section(self):
        return sorted([(self.education_order, self.display_education),(self.experience_order, self.display_experience),(self.skills_order, self.display_skills),(self.project_order, self.display_projects),(self.certification_order, self.display_certification)], key=lambda x: x[0])

    def display_contact(self):
        print("-"*20 + "Contact" + "-"*20)
        for every_key, every_value in self.contact.items():
            if every_key == "address":
                print("Address:")
                for address_key, address_value in every_value.items():
                    print(f"\t {address_key}: {address_value}")
            else:
                print(f"{every_key}: {every_value}")
    
    def display_education(self):
        print("-"*20 + "Education" + "-"*20)
        for school in self.education:
            print(f"Name: {school.name}")
            print(f"Major: {school.major}")
            print(f"GPA: {school.gpa}")
            print(f"Degree: {school.degree}")
            print(f"Related Courses: {', '.join(school.related_courses)}")
            print("-"*20)
    
    def display_experience(self):
        print("-"*20 + "Experience" + "-"*20)
        for job in self.experience:
            print(f"Job Title: {job.job_title}")
            print(f"Company: {job.company}")
            print(f"Duration: {job.duration}")
            print(f"Skills Used: {', '.join(job.skills_used)}")
            joined_summary = '\n - '.join(job.summary)
            print(f"Summary:\n - {joined_summary}")
            print("-"*20)
    
    def display_skills(self):
        print("-"*20 + "Skills" + "-"*20)
        for skill in self.skills:
            print(f"Category: {skill.category}")
            print(f"Skills: {', '.join(skill.skill)}")
            print("-"*20)
    
    def display_projects(self):
        print("-"*20 + "Projects" + "-"*20) 
        for project in self.projects:
            print(f"Project Name: {project.project_name}")
            print(f"Skills Used: {', '.join(project.skills_used)}")
            joined_summary = '\n - '.join(project.summary)
            print(f"Summary:\n - {joined_summary}")
            print("-"*20)
    
    def display_certification(self):
        print("-"*20 + "Certifications" + "-"*20)
        for cert in self.certification:
            print(f"Name: {cert.name}")
            print(f"Link: {cert.link}")
            print("-"*20)


class Education:
    def __init__(self, name, major, gpa, degree, related_courses):
        self.name = name
        self.major = major
        self.gpa = gpa
        self.degree = degree
        self.related_courses = related_courses

class Project:
    def __init__(self, project_name, skills_used, summary):
        self.project_name = project_name
        self.skills_used = skills_used
        self.summary = summary

class Experience:
    def __init__(self, job_title, company, duration, skills_used, summary):
        self.job_title = job_title
        self.company = company
        self.duration = duration
        self.skills_used = skills_used
        self.summary = summary

class Certification:
    def __init__(self, name, link):
        self.name = name
        self.link = link

class Skills:
    def __init__(self, category, skill):
        self.category = category
        self.skill = skill
        

