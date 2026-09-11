from recruiter_chat import (
    run_agent,
    handle_natural_language_query
)


JOB_DESCRIPTION = """
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


def run_flow(flow_number, user_input, result):
    print("\n")
    print("=" * 70)
    print(f"CONVERSATION FLOW {flow_number}")
    print("=" * 70)

    print(f"\nRecruiter: {user_input}")

    handle_natural_language_query(
        user_input,
        result,
        JOB_DESCRIPTION
    )


print("=" * 70)
print("STARTING RECRUITER CONVERSATION TESTS")
print("=" * 70)


# --------------------------------------------------
# Initial Agent Run
# --------------------------------------------------

print("\nRunning initial recruitment analysis...")

result = run_agent(
    JOB_DESCRIPTION
)


# --------------------------------------------------
# Flow 1 - Ranking
# --------------------------------------------------

run_flow(
    1,
    "Who are the best candidates for this role?",
    result
)


# --------------------------------------------------
# Flow 2 - Candidate Comparison
# --------------------------------------------------

run_flow(
    2,
    "Compare Swetha R and Sathish Kumar",
    result
)


# --------------------------------------------------
# Flow 3 - Interview Questions
# --------------------------------------------------

run_flow(
    3,
    "Give me interview questions for Swetha R",
    result
)


# --------------------------------------------------
# Flow 4 - Screening Report
# --------------------------------------------------

run_flow(
    4,
    "Show me the screening report",
    result
)


# --------------------------------------------------
# Flow 5 - Recruiter Feedback
# --------------------------------------------------

run_flow(
    5,
    "Prioritize candidates with strong AWS experience",
    result
)


print("\n")
print("=" * 70)
print("ALL 5 CONVERSATION FLOWS COMPLETED")
print("=" * 70)