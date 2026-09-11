from src.matching_agent import matching_agent
from src.agent_tools import compare_candidates, generate_interview_questions
from langchain_openrouter import ChatOpenRouter
from src.config import OPENROUTER_MODEL


# ============================================================
# 1. RUN MAIN LANGGRAPH AGENT
# ============================================================

def run_agent(job_description: str):
    """
    Run the complete LangGraph resume matching workflow.
    """

    state = {
        "conversation_history": [],
        "job_description": job_description,
        "human_feedback": "",
        "feedback_applied": False,
    }

    return matching_agent.invoke(state)


# ============================================================
# 2. UNDERSTAND RECRUITER QUERY
# ============================================================

def understand_recruiter_query(user_input: str) -> str:
    """
    Classify the recruiter's natural-language request.
    """

    model = ChatOpenRouter(
        model=OPENROUTER_MODEL,
        temperature=0
    )

    prompt = f"""
You are an AI recruiter assistant.

Classify the recruiter request into exactly ONE category.

Categories:

- ranking
- compare
- interview
- report
- feedback
- unknown

Examples:

"Who are the best candidates?"
-> ranking

"Show me the top candidates"
-> ranking

"Compare Swetha and Sathish"
-> compare

"Who is better between Swetha and Sathish?"
-> compare

"Give me interview questions for Swetha"
-> interview

"Show me the screening report"
-> report

"Prioritize candidates with strong AWS experience"
-> feedback

"Move Python experience higher in importance"
-> feedback

Return ONLY the category name.

Recruiter request:
{user_input}
"""

    response = model.invoke(prompt)

    category = response.content.strip().lower()

    valid_categories = {
        "ranking",
        "compare",
        "interview",
        "report",
        "feedback",
        "unknown"
    }

    if category not in valid_categories:
        return "unknown"

    return category


# ============================================================
# 3. DISPLAY RANKING
# ============================================================

def display_ranking(result):
    """
    Display top-ranked candidates in a clean format.
    """

    rankings = result.get("ranking_results", [])

    if not rankings:
        print("\nNo ranking results available.\n")
        return

    print("\n" + "=" * 70)
    print("TOP CANDIDATES")
    print("=" * 70)

    for index, candidate in enumerate(rankings, start=1):

        name = candidate.get("candidate_name", "Unknown")
        score = candidate.get("match_score", 0)
        skills = candidate.get("matched_skills", [])
        reasoning = candidate.get("reasoning", "")

        print(f"\n#{index} {name}")
        print(f"Match Score : {score:.2f}")

        if skills:
            print(
                "Matched Skills : "
                + ", ".join(skills)
            )

        if reasoning:
            print(f"Reasoning : {reasoning}")

    print("\n" + "=" * 70)


# ============================================================
# 4. EXTRACT TWO CANDIDATE NAMES
# ============================================================

def extract_compare_names(user_input: str):

    text = user_input.strip()

    prefixes = [
        "compare candidates ",
        "compare candidate ",
        "compare "
    ]

    lower_text = text.lower()

    for prefix in prefixes:

        if lower_text.startswith(prefix):
            text = text[len(prefix):]
            break

    if " and " not in text.lower():
        return []

    parts = text.split(" and ", 1)

    if len(parts) != 2:
        return []

    candidate_1 = parts[0].strip()
    candidate_2 = parts[1].strip()

    if not candidate_1 or not candidate_2:
        return []

    return [candidate_1, candidate_2]


# ============================================================
# 5. EXTRACT INTERVIEW CANDIDATE
# ============================================================

def extract_interview_candidate(user_input: str):

    text = user_input.strip()

    prefixes = [
        "give me interview questions for ",
        "generate interview questions for ",
        "interview questions for ",
        "interview "
    ]

    lower_text = text.lower()

    for prefix in prefixes:

        if lower_text.startswith(prefix):
            return text[len(prefix):].strip()

    return text


# ============================================================
# 6. DISPLAY COMPARISON
# ============================================================

def display_comparison(comparison_results):

    if not comparison_results:
        print("\nNo matching candidates found.\n")
        return

    print("\n" + "=" * 70)
    print("HEAD-TO-HEAD CANDIDATE COMPARISON")
    print("=" * 70)

    for index, candidate in enumerate(
        comparison_results,
        start=1
    ):

        print(f"\nCandidate {index}")
        print("-" * 50)

        print(
            f"Name : "
            f"{candidate.get('candidate_name', 'Unknown')}"
        )

        print(
            f"Score : "
            f"{candidate.get('match_score', 0):.2f}"
        )

        skills = candidate.get("matched_skills", [])

        if skills:
            print(
                "Matched Skills : "
                + ", ".join(skills)
            )

        reasoning = candidate.get("reasoning", "")

        if reasoning:
            print(f"Reasoning : {reasoning}")

    print("\n" + "=" * 70)


# ============================================================
# 7. DISPLAY INTERVIEW QUESTIONS
# ============================================================

def display_interview_questions(candidate_name, questions):

    print("\n" + "=" * 70)
    print(f"INTERVIEW QUESTIONS — {candidate_name}")
    print("=" * 70)

    if isinstance(questions, list):

        for index, question in enumerate(
            questions,
            start=1
        ):
            print(f"\n{index}. {question}")

    else:
        print("\n" + str(questions))

    print("\n" + "=" * 70)


# ============================================================
# 8. DISPLAY RANKING CHANGES
# ============================================================

def display_ranking_changes(result):

    changes = result.get("ranking_changes", [])

    print("\n" + "=" * 70)
    print("RANKING CHANGES")
    print("=" * 70)

    if not changes:
        print("\nNo ranking changes detected.")
        print(
            "The recruiter preference was applied, "
            "but the relative ranking remained the same."
        )
        print("\n" + "=" * 70)
        return

    for change in changes:

        name = change.get(
            "candidate_name",
            "Unknown"
        )

        old_position = change.get(
            "old_position",
            "-"
        )

        new_position = change.get(
            "new_position",
            "-"
        )

        old_score = change.get(
            "old_score",
            0
        )

        new_score = change.get(
            "new_score",
            0
        )

        print(f"\n{name}")

        print(
            f"Position : "
            f"#{old_position} -> #{new_position}"
        )

        print(
            f"Score    : "
            f"{old_score:.2f} -> {new_score:.2f}"
        )

    print("\n" + "=" * 70)


# ============================================================
# 9. HANDLE NATURAL LANGUAGE QUERY
# ============================================================

def handle_natural_language_query(
    user_input,
    result,
    job_description
):

    intent = understand_recruiter_query(user_input)

    print(f"\n[Intent detected: {intent}]")

    # --------------------------------------------------------
    # RANKING
    # --------------------------------------------------------

    if intent == "ranking":

        display_ranking(result)

    # --------------------------------------------------------
    # COMPARE
    # --------------------------------------------------------

    elif intent == "compare":

        candidate_ids = extract_compare_names(user_input)

        if len(candidate_ids) != 2:

            print(
                "\nPlease provide two candidate names."
            )

            print(
                "Example: "
                "Compare Swetha R and Sathish Kumar"
            )

            return

        comparison = compare_candidates(
            candidate_ids,
            job_description
        )

        display_comparison(comparison)

    # --------------------------------------------------------
    # INTERVIEW
    # --------------------------------------------------------

    elif intent == "interview":

        candidate_name = extract_interview_candidate(
            user_input
        )

        if not candidate_name:

            print(
                "\nPlease provide a candidate name."
            )

            return

        questions = generate_interview_questions(
            candidate_name,
            job_description
        )

        display_interview_questions(
            candidate_name,
            questions
        )

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    elif intent == "report":

        report = result.get(
            "final_report",
            "No report available."
        )

        print("\n" + "=" * 70)
        print("SCREENING REPORT")
        print("=" * 70)

        print(report)

        print("\n" + "=" * 70)

    # --------------------------------------------------------
    # FEEDBACK
    # --------------------------------------------------------

    elif intent == "feedback":

        print(
            "\nApplying recruiter feedback..."
        )

        feedback_state = {
            "conversation_history": result.get(
                "conversation_history",
                []
            ),

            "job_description": job_description,

            "human_feedback": user_input,

            "feedback_applied": False,

            "ranking_results": result.get(
                "ranking_results",
                []
            ),

            "previous_ranking_results": result.get(
                "ranking_results",
                []
            )
        }

        updated_result = matching_agent.invoke(
            feedback_state
        )

        print(
            "\nRecruiter preference applied successfully."
        )

        print(
            f"\nUpdated Job Description:\n"
            f"{updated_result.get('job_description', '')}"
        )

        display_ranking(updated_result)

        display_ranking_changes(updated_result)

        return updated_result

    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    else:

        print(
            "\nSorry, I couldn't understand that request."
        )

        print(
            "\nTry something like:"
        )

        print(
            "• Who are the best candidates?"
        )

        print(
            "• Compare Candidate A and Candidate B"
        )

        print(
            "• Give me interview questions for Candidate A"
        )

        print(
            "• Show me the screening report"
        )

        print(
            "• Prioritize candidates with strong AWS experience"
        )

    return result


# ============================================================
# 10. INTERACTIVE RECRUITER CHAT
# ============================================================

def start_recruiter_chat():

    print("\n" + "=" * 70)
    print("AI RESUME MATCHING AGENT")
    print("LangGraph + RAG + LLM Recruitment Assistant")
    print("=" * 70)

    print("\nChoose how to provide the Job Description:")
    print("1. Enter JD text")
    print("2. Load JD from file")

    choice = input("\nEnter choice (1/2): ").strip()

    if choice == "2":

        jd_path = input(
            "\nEnter JD file path: "
        ).strip()

        try:

            with open(
                jd_path,
                "r",
                encoding="utf-8"
            ) as file:

                job_description = file.read().strip()

            if not job_description:

                print(
                    "\nJob description file is empty."
                )

                return

            print(
                f"\nLoaded Job Description from: "
                f"{jd_path}"
            )

        except FileNotFoundError:

            print(
                f"\nFile not found: {jd_path}"
            )

            return

        except Exception as error:

            print(
                f"\nUnable to read JD file: {error}"
            )

            return

    else:

        print(
            "\nEnter the Job Description "
            "in one line:"
        )

        job_description = input(
            "\nJD: "
        ).strip()

        if not job_description:

            print(
                "\nJob description cannot be empty."
            )

            return
    
    print("\nRunning initial candidate matching...")

    result = run_agent(job_description)

    print("\nInitial matching completed successfully.")

    display_ranking(result)

    print("\n" + "=" * 70)
    print("RECRUITER CHAT MODE")
    print("=" * 70)

    print(
        "\nYou can ask:"
        "\n• Who are the best candidates?"
        "\n• Compare two candidates"
        "\n• Give me interview questions for a candidate"
        "\n• Show me the screening report"
        "\n• Prioritize candidates with a specific skill"
        "\n\nType 'exit' or 'quit' to stop."
)

    current_result = result
    current_job_description = job_description

    while True:

        print()

        user_input = input(
            "Recruiter: "
        ).strip()

        if not user_input:
            continue

        if user_input.lower() in {
            "exit",
            "quit",
            "q"
        }:

            print(
                "\nAI Agent session ended. "
                "Thank you!"
            )

            break

        try:

            updated_result = (
                handle_natural_language_query(
                    user_input,
                    current_result,
                    current_job_description
                )
            )

            if updated_result is not None:

                current_result = updated_result

                current_job_description = (
                    updated_result.get(
                        "job_description",
                        current_job_description
                    )
                )

        except Exception as error:

            print(
                "\nSomething went wrong while "
                "processing your request."
            )

            print(
                f"Error: {error}"
            )


# ============================================================
# 11. APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    start_recruiter_chat()