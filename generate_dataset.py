from pathlib import Path


RESUME_DIR = Path("resumes")
JD_DIR = Path("job_descriptions")


RESUME_DIR.mkdir(exist_ok=True)
JD_DIR.mkdir(exist_ok=True)


resumes = [
    {
        "name": "Arun Kumar",
        "filename": "arun_kumar.txt",
        "skills": "Python, Django, FastAPI, PostgreSQL, Docker, AWS, Git",
        "experience": "6 years of experience developing backend applications and REST APIs using Python, Django and FastAPI.",
        "education": "B.Tech in Computer Science",
        "projects": "Built scalable REST APIs and deployed microservices on AWS."
    },
    {
        "name": "Priya Sharma",
        "filename": "priya_sharma.txt",
        "skills": "Python, Machine Learning, TensorFlow, PyTorch, Pandas, NumPy, AWS",
        "experience": "5 years of experience building machine learning models and production ML pipelines.",
        "education": "M.Tech in Artificial Intelligence",
        "projects": "Developed classification and prediction models using TensorFlow and PyTorch."
    },
    {
        "name": "Rahul Verma",
        "filename": "rahul_verma.txt",
        "skills": "Java, Spring Boot, MySQL, Docker, Kubernetes, AWS",
        "experience": "7 years of experience developing enterprise backend applications using Java and Spring Boot.",
        "education": "B.Tech in Information Technology",
        "projects": "Developed distributed enterprise services and containerized applications."
    },
    {
        "name": "Sneha Rao",
        "filename": "sneha_rao.txt",
        "skills": "Python, Django, PostgreSQL, React, Docker",
        "experience": "4 years of experience developing full stack web applications using Python and React.",
        "education": "B.E. Computer Science",
        "projects": "Built customer management applications using Django, React and PostgreSQL."
    },
    {
        "name": "Vikram Singh",
        "filename": "vikram_singh.txt",
        "skills": "Python, FastAPI, PostgreSQL, Redis, Docker, AWS",
        "experience": "8 years of experience designing high-performance Python backend systems.",
        "education": "B.Tech Computer Science",
        "projects": "Designed scalable APIs and distributed backend services."
    },
    {
        "name": "Ananya Iyer",
        "filename": "ananya_iyer.txt",
        "skills": "Python, Pandas, NumPy, SQL, Machine Learning, Scikit-learn",
        "experience": "4 years of experience in data science and predictive analytics.",
        "education": "M.Sc. Data Science",
        "projects": "Created predictive models and customer analytics dashboards."
    },
    {
        "name": "Karthik Raj",
        "filename": "karthik_raj.txt",
        "skills": "AWS, Docker, Kubernetes, Terraform, Linux, CI/CD, Git",
        "experience": "6 years of experience working as a DevOps and cloud engineer.",
        "education": "B.Tech Information Technology",
        "projects": "Built CI/CD pipelines and managed Kubernetes infrastructure on AWS."
    },
    {
        "name": "Divya Menon",
        "filename": "divya_menon.txt",
        "skills": "React, JavaScript, TypeScript, Node.js, PostgreSQL, AWS",
        "experience": "5 years of experience building modern frontend and full stack applications.",
        "education": "B.Tech Computer Science",
        "projects": "Developed React applications and Node.js backend services."
    },
    {
        "name": "Suresh Kumar",
        "filename": "suresh_kumar.txt",
        "skills": "Python, FastAPI, Django, MySQL, Docker",
        "experience": "3 years of experience developing Python backend APIs.",
        "education": "B.E. Computer Science",
        "projects": "Built REST APIs for business applications."
    },
    {
        "name": "Meera Krishnan",
        "filename": "meera_krishnan.txt",
        "skills": "Python, PyTorch, Deep Learning, Machine Learning, NumPy",
        "experience": "6 years of experience developing deep learning models and computer vision solutions.",
        "education": "M.Tech Artificial Intelligence",
        "projects": "Built deep learning image classification systems using PyTorch."
    },
    {
        "name": "Aditya Patel",
        "filename": "aditya_patel.txt",
        "skills": "Python, SQL, Pandas, NumPy, Machine Learning",
        "experience": "5 years of experience in data analytics and machine learning.",
        "education": "M.Sc. Statistics",
        "projects": "Developed forecasting and customer segmentation models."
    },
    {
        "name": "Nisha Thomas",
        "filename": "nisha_thomas.txt",
        "skills": "JavaScript, React, Angular, TypeScript, Node.js",
        "experience": "6 years of experience developing frontend and full stack applications.",
        "education": "B.Tech Information Technology",
        "projects": "Developed enterprise dashboards and web applications."
    },
    {
        "name": "Manoj Kumar",
        "filename": "manoj_kumar.txt",
        "skills": "Python, Flask, PostgreSQL, Docker, AWS",
        "experience": "5 years of experience developing Python web applications and APIs.",
        "education": "B.Tech Computer Science",
        "projects": "Developed Flask APIs and cloud applications."
    },
    {
        "name": "Harini S",
        "filename": "harini_s.txt",
        "skills": "Python, Machine Learning, TensorFlow, Pandas, SQL",
        "experience": "3 years of experience working on machine learning and data science projects.",
        "education": "M.Sc. Data Science",
        "projects": "Built machine learning models for customer prediction."
    },
    {
        "name": "Rohit Gupta",
        "filename": "rohit_gupta.txt",
        "skills": "AWS, Azure, Docker, Kubernetes, Terraform, Linux",
        "experience": "8 years of experience in cloud infrastructure and DevOps.",
        "education": "B.Tech Information Technology",
        "projects": "Managed cloud infrastructure and Kubernetes clusters."
    },
    {
        "name": "Lakshmi Devi",
        "filename": "lakshmi_devi.txt",
        "skills": "Python, Django, FastAPI, PostgreSQL, AWS, Docker",
        "experience": "7 years of experience developing Python backend systems.",
        "education": "B.E. Computer Science",
        "projects": "Built scalable backend APIs and cloud-native applications."
    },
    {
        "name": "Aakash Reddy",
        "filename": "aakash_reddy.txt",
        "skills": "Python, LLM, Machine Learning, FastAPI, PyTorch, Docker",
        "experience": "4 years of experience developing AI and machine learning applications.",
        "education": "M.Tech Artificial Intelligence",
        "projects": "Built LLM-powered applications and AI APIs."
    },
    {
        "name": "Pooja Nair",
        "filename": "pooja_nair.txt",
        "skills": "Python, Data Science, Pandas, NumPy, SQL, Scikit-learn",
        "experience": "6 years of experience working in data science and analytics.",
        "education": "M.Sc. Data Science",
        "projects": "Built predictive analytics and business intelligence solutions."
    },
    {
        "name": "Vivek Shah",
        "filename": "vivek_shah.txt",
        "skills": "Java, Spring Boot, PostgreSQL, Docker, AWS",
        "experience": "5 years of experience building Java backend microservices.",
        "education": "B.Tech Computer Science",
        "projects": "Built microservices using Spring Boot and Docker."
    },
    {
        "name": "Swetha R",
        "filename": "swetha_r.txt",
        "skills": "Python, FastAPI, PostgreSQL, AWS, Docker",
        "experience": "6 years of experience developing backend APIs with Python.",
        "education": "B.Tech Information Technology",
        "projects": "Designed FastAPI services deployed on AWS."
    },
    {
        "name": "Aravind Kumar",
        "filename": "aravind_kumar.txt",
        "skills": "React, Node.js, JavaScript, MongoDB, Docker",
        "experience": "4 years of experience developing full stack web applications.",
        "education": "B.E. Computer Science",
        "projects": "Developed scalable React and Node.js applications."
    },
    {
        "name": "Deepa Joseph",
        "filename": "deepa_joseph.txt",
        "skills": "Python, TensorFlow, PyTorch, Deep Learning, Machine Learning",
        "experience": "7 years of experience in deep learning and artificial intelligence.",
        "education": "Ph.D. Artificial Intelligence",
        "projects": "Developed neural network models for image and text processing."
    },
    {
        "name": "Ganesh B",
        "filename": "ganesh_b.txt",
        "skills": "Docker, Kubernetes, AWS, Terraform, Linux, CI/CD",
        "experience": "5 years of experience in DevOps and cloud automation.",
        "education": "B.Tech Computer Science",
        "projects": "Automated cloud deployments and Kubernetes infrastructure."
    },
    {
        "name": "Riya Kapoor",
        "filename": "riya_kapoor.txt",
        "skills": "Python, Django, MySQL, REST APIs, Git",
        "experience": "2 years of experience developing Python web applications.",
        "education": "B.Tech Computer Science",
        "projects": "Developed Django-based business applications."
    },
    {
        "name": "Sanjay Rao",
        "filename": "sanjay_rao.txt",
        "skills": "Python, FastAPI, PostgreSQL, Redis, AWS",
        "experience": "9 years of experience designing distributed backend systems.",
        "education": "B.Tech Computer Science",
        "projects": "Designed high-scale APIs and event-driven backend systems."
    },
    {
        "name": "Keerthi Anand",
        "filename": "keerthi_anand.txt",
        "skills": "Python, Machine Learning, LLM, FastAPI, NLP",
        "experience": "5 years of experience developing natural language processing and AI applications.",
        "education": "M.Tech Artificial Intelligence",
        "projects": "Built NLP and LLM-powered applications."
    },
    {
        "name": "Varun Joshi",
        "filename": "varun_joshi.txt",
        "skills": "AWS, Docker, Kubernetes, Linux, Terraform",
        "experience": "4 years of experience managing cloud infrastructure.",
        "education": "B.Tech Information Technology",
        "projects": "Managed AWS infrastructure and containerized deployments."
    },
    {
        "name": "Ishita Roy",
        "filename": "ishita_roy.txt",
        "skills": "Python, Pandas, NumPy, SQL, Machine Learning, Scikit-learn",
        "experience": "5 years of experience in data science and predictive modeling.",
        "education": "M.Sc. Data Science",
        "projects": "Developed recommendation and prediction systems."
    },
    {
        "name": "Mohan Das",
        "filename": "mohan_das.txt",
        "skills": "JavaScript, React, TypeScript, Node.js, MongoDB",
        "experience": "3 years of experience developing full stack applications.",
        "education": "B.Tech Computer Science",
        "projects": "Built responsive web applications and APIs."
    },
    {
        "name": "Sathish Kumar",
        "filename": "sathish_kumar.txt",
        "skills": "Python, Django, FastAPI, PostgreSQL, Docker, AWS",
        "experience": "5 years of experience developing Python backend applications.",
        "education": "B.Tech Computer Science",
        "projects": "Built REST APIs and deployed backend applications on AWS."
    },
    {
        "name": "Neha Singh",
        "filename": "neha_singh.txt",
        "skills": "Python, PyTorch, Machine Learning, Deep Learning, LLM",
        "experience": "6 years of experience in artificial intelligence and deep learning.",
        "education": "M.Tech Artificial Intelligence",
        "projects": "Developed deep learning and LLM-based AI solutions."
    },
    {
        "name": "Tarun Mehta",
        "filename": "tarun_mehta.txt",
        "skills": "Python, Java, SQL, Docker, AWS",
        "experience": "4 years of experience developing backend and cloud applications.",
        "education": "B.Tech Computer Science",
        "projects": "Built backend services and cloud deployment solutions."
    }
]


job_descriptions = {
    "python_backend_engineer.txt": """
Python Backend Engineer

We are looking for a backend engineer with 5+ years of experience.

Must-have requirements:
- Python
- FastAPI
- Django
- PostgreSQL
- Docker
- AWS

Experience with REST APIs and scalable backend systems is preferred.
""",

    "machine_learning_engineer.txt": """
Machine Learning Engineer

We are looking for a machine learning engineer with 3+ years of experience.

Must-have requirements:
- Python
- Machine Learning
- PyTorch
- TensorFlow
- Scikit-learn
- AWS

Experience building production machine learning systems is preferred.
""",

    "data_scientist.txt": """
Data Scientist

We are looking for a data scientist with 4+ years of experience.

Must-have requirements:
- Python
- Pandas
- NumPy
- SQL
- Machine Learning
- Scikit-learn

Experience with predictive analytics is preferred.
""",

    "full_stack_engineer.txt": """
Full Stack Engineer

We are looking for a full stack engineer with 4+ years of experience.

Must-have requirements:
- React
- Node.js
- JavaScript
- PostgreSQL
- Docker
- AWS
""",

    "devops_engineer.txt": """
DevOps Engineer

We are looking for a DevOps engineer with 5+ years of experience.

Must-have requirements:
- AWS
- Docker
- Kubernetes
- Terraform
- Linux
- CI/CD

Experience with cloud automation is preferred.
""",

    "ai_engineer.txt": """
AI Engineer

We are looking for an AI engineer with 3+ years of experience.

Must-have requirements:
- Python
- Machine Learning
- Deep Learning
- PyTorch
- LLM
- FastAPI

Experience building AI-powered applications is preferred.
"""
}


def create_resume(resume):
    content = f"""Name
{resume['name']}

Skills
{resume['skills']}

Experience
{resume['experience']}

Education
{resume['education']}

Projects
{resume['projects']}
"""

    filepath = RESUME_DIR / resume["filename"]

    filepath.write_text(
        content,
        encoding="utf-8"
    )


def create_job_description(filename, content):
    filepath = JD_DIR / filename

    filepath.write_text(
        content.strip(),
        encoding="utf-8"
    )


def main():
    print("Creating synthetic resume dataset...")

    for resume in resumes:
        create_resume(resume)

    print(f"Created {len(resumes)} resumes.")

    print("\nCreating job descriptions...")

    for filename, content in job_descriptions.items():
        create_job_description(
            filename,
            content
        )

    print(
        f"Created {len(job_descriptions)} job descriptions."
    )

    print("\nDataset generation completed.")


if __name__ == "__main__":
    main()