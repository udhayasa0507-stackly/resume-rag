from src.matching_agent import matching_agent

from deep_screening import deep_screen_candidates


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
    "human_feedback": "",
    "feedback_applied": False,
}


result = matching_agent.invoke(state)

top_10 = result.get(
    "ranking_results",
    []
)[:10]

print("\n" + "=" * 60)
print("ROUND 1 - TOP 10")
print("=" * 60)

for index, candidate in enumerate(
    top_10,
    start=1
):
    print(
        f"{index}. "
        f"{candidate['candidate_name']} "
        f"-> {candidate['match_score']}"
    )


print("\n" + "=" * 60)
print("ROUND 2 - DEEP SCREENING")
print("=" * 60)

deep_results = deep_screen_candidates(
    job_description,
    top_10
)

for result in deep_results:
    print("\nCandidate:", result["candidate_name"])
    print(
        "Initial Score:",
        result["initial_match_score"]
    )
    print("Deep Analysis:")
    print(result["deep_analysis"])