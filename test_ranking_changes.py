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


state = {
    "conversation_history": [],
    "job_description": job_description,
    "human_feedback": "Prioritize candidates with strong AWS experience.",
    "feedback_applied": False,
}


result = matching_agent.invoke(state)


print("\n" + "=" * 60)
print("RANKING CHANGES")
print("=" * 60)

ranking_changes = result.get("ranking_changes", [])

if not ranking_changes:
    print("No ranking changes detected.")
else:
    for change in ranking_changes:
        print(
            f"{change['candidate_name']}: "
            f"Position {change['old_position']} -> "
            f"{change['new_position']} | "
            f"Score {change['old_score']} -> "
            f"{change['new_score']} | "
            f"Score Change: {change['score_change']} | "
            f"{change['change']}"
        )