from src.matching_agent import matching_agent


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


state = {
    "conversation_history": [],
    "job_description": job_description,
    "human_feedback": "",
    "feedback_applied": False,
}


print("=" * 60)
print("RUNNING COMPLETE LANGGRAPH AGENT")
print("=" * 60)


result = matching_agent.invoke(state)


print("\n" + "=" * 60)
print("FINAL RESULTS")
print("=" * 60)


print("\nTOP CANDIDATES:")
for index, candidate in enumerate(
    result.get("ranking_results", []),
    start=1
):
    print(
        f"{index}. "
        f"{candidate['candidate_name']} "
        f"-> {candidate['match_score']}"
    )


print("\nDEEP SCREENING:")

for candidate in result.get(
    "deep_screening_results",
    []
):

    analysis = candidate["deep_analysis"]

    print(
        f"\n{candidate['candidate_name']}"
    )

    print(
        f"Initial Score: "
        f"{candidate['initial_match_score']}"
    )

    print(
        f"Deep Score: "
        f"{analysis.get('deep_score')}"
    )

    print(
        f"Recommendation: "
        f"{analysis.get('recommendation')}"
    )


print("\nFINAL DECISIONS:")

for decision in result.get(
    "final_decisions",
    []
):

    print(
        f"\n{decision['candidate_name']}"
    )

    print(
        f"Decision: "
        f"{decision['final_decision']}"
    )

    print(
        f"Final Score: "
        f"{decision['final_score']}"
    )

    print(
        f"Reason: "
        f"{decision['reason']}"
    )


print("\n" + "=" * 60)
print("LANGGRAPH WORKFLOW COMPLETED")
print("=" * 60)