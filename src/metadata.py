import re


COMMON_SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C++",
    "C#",
    "Django",
    "FastAPI",
    "Flask",
    "React",
    "Angular",
    "Node.js",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "Redis",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "SQL",
    "Git",
]


def skill_exists(skill: str, text: str) -> bool:
    """
    Check whether a skill appears as a complete term.

    Example:
    PostgreSQL  -> does NOT match SQL
    SQL         -> matches SQL
    Python      -> matches Python
    """

    pattern = (
        r"(?<![a-zA-Z0-9])"
        + re.escape(skill)
        + r"(?![a-zA-Z0-9])"
    )

    return re.search(
        pattern,
        text,
        re.IGNORECASE
    ) is not None


def extract_name(text: str) -> str:
    """
    Extract candidate name from the resume.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return "Unknown"

    if lines[0].lower() == "name" and len(lines) > 1:
        return lines[1]

    return lines[0]


def extract_skills(text: str) -> list[str]:
    """
    Extract technical skills from resume text.
    """

    found_skills = []

    for skill in COMMON_SKILLS:

        if skill_exists(skill, text):
            found_skills.append(skill)

    return found_skills


def extract_experience_years(text: str) -> float:
    """
    Extract years of professional experience.
    """

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+experience",
        r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\+?\s*years?"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return float(match.group(1))

    return 0.0


def extract_education(text: str) -> str:
    """
    Extract education information.
    """

    lines = text.splitlines()

    education_started = False
    education_lines = []

    stop_sections = [
        "experience",
        "work experience",
        "skills",
        "projects",
        "certifications",
        "achievements",
        "languages"
    ]

    for line in lines:

        cleaned = line.strip()

        if not cleaned:
            continue

        if cleaned.lower() in [
            "education",
            "academic background",
            "educational background"
        ]:

            education_started = True
            continue

        if education_started:

            if cleaned.lower() in stop_sections:
                break

            education_lines.append(cleaned)

    return " ".join(education_lines).strip()


def extract_metadata(text: str) -> dict:
    """
    Extract all important resume metadata.
    """

    return {
        "candidate_name": extract_name(text),
        "skills": extract_skills(text),
        "experience_years": extract_experience_years(text),
        "education": extract_education(text)
    }