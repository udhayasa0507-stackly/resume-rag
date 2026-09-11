from src.matching_agent import matching_agent
from deep_screening import deep_screen_candidates
from final_decision import make_final_decisions


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
print("ROUND 1 - INITIAL MATCHING")
print("=" * 60)

state = {
    "conversation_history": [],
    "job_description": job_description,
    "human_feedback": "",
    "feedback_applied": False,
}

result = matching_agent.invoke(state)

top_10 = result["ranking_results"]

for index, candidate in enumerate(top_10, start=1):
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

for candidate in deep_results:

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


print("\n" + "=" * 60)
print("ROUND 3 - FINAL HIRING DECISION")
print("=" * 60)

final_decisions = make_final_decisions(
    job_description,
    deep_results
)

for decision in final_decisions:

    print(
        f"\nCandidate: "
        f"{decision['candidate_name']}"
    )

    print(
        f"Final Decision: "
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

    print(
        f"Strengths: "
        f"{decision['key_strengths']}"
    )

    print(
        f"Gaps: "
        f"{decision['key_gaps']}"
    )