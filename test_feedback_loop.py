from src.matching_agent import matching_agent


job_description = """
We are looking for a Python Backend Engineer.

Requirements:
- 3+ years of experience
- Python
- FastAPI
- PostgreSQL
- Docker
- AWS
"""


initial_state = {
    "conversation_history": [],
    "job_description": job_description,
    "human_feedback": "Prioritize candidates with strong AWS experience.",
    "feedback_applied": False,
}


result = matching_agent.invoke(initial_state)


print("\n" + "=" * 60)
print("RANKING AFTER RECRUITER FEEDBACK")
print("=" * 60)

for candidate in result.get("ranking_results", [])[:3]:
    print(
        candidate["candidate_name"],
        "->",
        candidate["match_score"]
    )


print("\n" + "=" * 60)
print("UPDATED JOB DESCRIPTION")
print("=" * 60)

print(result.get("job_description", ""))


print("\n" + "=" * 60)
print("UPDATED FINAL REPORT")
print("=" * 60)

print(result.get("final_report", "No report"))