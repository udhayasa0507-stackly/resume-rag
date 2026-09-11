from recruiter_chat import (
    run_agent,
    handle_natural_language_query
)


job_description = """
We are hiring a Python Backend Engineer.

Requirements:
- 3+ years of experience
- Python
- FastAPI
- PostgreSQL

Nice to have:
- Docker
- AWS

The candidate should have strong backend
API development experience.
"""


print("=" * 60)
print("RUNNING INITIAL AGENT")
print("=" * 60)

result = run_agent(
    job_description
)


user_input = (
    "Prioritize candidates with strong AWS experience."
)

print("\n" + "=" * 60)
print("RECRUITER QUERY")
print("=" * 60)

print(
    f"Recruiter: {user_input}"
)


handle_natural_language_query(
    user_input,
    result,
    job_description
)