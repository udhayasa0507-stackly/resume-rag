from src.matching_agent import matching_agent


def main():
    print("=" * 60)
    print("🤖 Resume RAG - AI Recruitment Agent")
    print("=" * 60)

    print("\nEnter the Job Description.")
    print("Type 'END' on a new line when finished.\n")

    jd_lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        jd_lines.append(line)

    job_description = "\n".join(jd_lines).strip()

    if not job_description:
        print("No job description provided.")
        return

    print("\nProcessing job description...\n")

    state = {
        "conversation_history": [],
        "job_description": job_description,
        "human_feedback": "",
        "feedback_applied": False,
    }

    result = matching_agent.invoke(state)

    print("\n" + "=" * 60)
    print("TOP CANDIDATES")
    print("=" * 60)

    ranking_results = result.get("ranking_results", [])

    for index, candidate in enumerate(
        ranking_results[:10],
        start=1
    ):
        print(
            f"{index}. "
            f"{candidate['candidate_name']} "
            f"-> {candidate['match_score']}"
        )

    print("\n" + "=" * 60)
    print("SCREENING REPORT")
    print("=" * 60)

    print(result.get("final_report", "No report generated."))


if __name__ == "__main__":
    main()