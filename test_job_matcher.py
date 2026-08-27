from src.resume_rag import ResumeRAG
from src.job_matcher import JobMatcher
import json


# Create RAG system
rag = ResumeRAG(
    resume_directory="resumes",
    chroma_directory="chroma_db"
)


# Create matcher
matcher = JobMatcher(rag)


# Job description
job_description = """
Python Backend Engineer

We are looking for a backend engineer with
5+ years of experience.

Requirements:
- Strong Python experience
- FastAPI
- Django
- PostgreSQL
- Docker
- AWS
"""


# Match candidates
result = matcher.match_job(
    job_description,
    top_k=10
)


print("\nJOB MATCHING RESULTS")
print("=" * 70)

print(
    json.dumps(
        result,
        indent=2
    )
)