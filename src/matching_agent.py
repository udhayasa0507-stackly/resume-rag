from langgraph.graph import StateGraph, START, END

from src.agent_state import AgentState
from src.agent_tools import rag, extract_requirements, rag_search_tool
from src.job_matcher import JobMatcher

from langchain_openrouter import ChatOpenRouter
from src.config import OPENROUTER_MODEL

from deep_screening import deep_screen_candidates
from final_decision import make_final_decisions


# --------------------------------------------------
# Node functions
# --------------------------------------------------

def parse_jd(state: AgentState) -> AgentState:
    """
    Parse and prepare the job description.
    """

    print("\n[Node] Parse JD")

    return state


def extract_requirements_node(
    state: AgentState
) -> AgentState:
    """
    Extract job requirements using the LLM.
    """

    print("[Node] Extract Requirements")

    job_description = state.get(
        "job_description",
        ""
    )

    if not job_description:
        return state

    requirements = extract_requirements(
        job_description
    )

    state["requirements"] = requirements

    return state


def search_resumes_node(
    state: AgentState
) -> AgentState:
    """
    Search relevant resumes using the RAG system.
    """

    print("[Node] Search Resumes")

    job_description = state.get(
        "job_description",
        ""
    )

    if not job_description:
        return state

    results = rag_search_tool(
        query=job_description,
        top_k=10
    )

    state["candidate_shortlist"] = results

    return state


def rank_candidates_node(
    state: AgentState
) -> AgentState:
    print("[Node] Rank Candidates")

    job_description = state.get("job_description", "")

    if not job_description:
        return state

    # Save the previous ranking before creating a new ranking
    previous_ranking = state.get("ranking_results", [])

    if previous_ranking:
        state["previous_ranking_results"] = previous_ranking

    matcher = JobMatcher(rag)

    match_result = matcher.match_job(
        job_description=job_description,
        top_k=10
    )

    new_ranking = match_result["top_matches"]

    state["ranking_results"] = new_ranking

    # Compare old and new rankings
    if previous_ranking:
        previous_positions = {
            candidate["candidate_name"]: index
            for index, candidate in enumerate(
                previous_ranking,
                start=1
            )
        }

        new_positions = {
            candidate["candidate_name"]: index
            for index, candidate in enumerate(
                new_ranking,
                start=1
            )
        }

        ranking_changes = []

        for candidate in new_ranking:
            name = candidate["candidate_name"]

            old_position = previous_positions.get(name)
            new_position = new_positions.get(name)

            if old_position is not None:
                position_change = old_position - new_position

                if position_change > 0:
                    change = "moved up"
                elif position_change < 0:
                    change = "moved down"
                else:
                    change = "position unchanged"

                ranking_changes.append({
                    "candidate_name": name,
                    "old_position": old_position,
                    "new_position": new_position,
                    "position_change": position_change,
                    "old_score": next(
                        (
                            candidate["match_score"]
                            for candidate in previous_ranking
                            if candidate["candidate_name"] == name
                        ),
                        None
                    ),
                    "new_score": candidate["match_score"],
                    "score_change": round(
                        candidate["match_score"]
                        - next(
                            (
                                previous_candidate["match_score"]
                                for previous_candidate in previous_ranking
                                if previous_candidate["candidate_name"] == name
                            ),
                            candidate["match_score"]
                        ),
                        2
                    ),
                    "change": change
                })

        state["ranking_changes"] = ranking_changes

    return state

def generate_report_node(
    state: AgentState
) -> AgentState:
    """
    Generate a recruiter-friendly candidate report
    using the LLM.
    """

    print("[Node] Generate Report")

    job_description = state.get(
        "job_description",
        ""
    )

    requirements = state.get(
        "requirements",
        {}
    )

    ranking_results = state.get(
        "ranking_results",
        []
    )

    if not ranking_results:
        state["final_report"] = (
            "No suitable candidates were found."
        )
        return state

    model = ChatOpenRouter(
        model=OPENROUTER_MODEL,
        temperature=0,
    )

    prompt = f"""
You are an expert technical recruiter.

Create a concise candidate screening report
based on the job description and candidate ranking.

JOB DESCRIPTION:
{job_description}

EXTRACTED REQUIREMENTS:
{requirements}

RANKED CANDIDATES:
{ranking_results}

For the report:

1. Identify the top 3 candidates.
2. Show their match scores.
3. Explain their strongest matching skills.
4. Mention important gaps if any.
5. Recommend the strongest candidate.
6. Give a short reason for the recommendation.

Use clear headings and bullet points.

Do not invent information that is not present
in the provided candidate data.
"""

    response = model.invoke(prompt)

    state["final_report"] = response.content

    return state

def deep_screening_node(
    state: AgentState
) -> AgentState:
    print("[Node] Deep Screening")

    job_description = state.get(
        "job_description",
        ""
    )

    candidates = state.get(
        "ranking_results",
        []
    )

    if not candidates:
        state["deep_screening_results"] = []
        return state

    deep_results = deep_screen_candidates(
        job_description,
        candidates
    )

    state["deep_screening_results"] = deep_results

    return state

def final_decision_node(
    state: AgentState
) -> AgentState:
    print("[Node] Final Decision")

    job_description = state.get(
        "job_description",
        ""
    )

    deep_results = state.get(
        "deep_screening_results",
        []
    )

    if not deep_results:
        state["final_decisions"] = []
        return state

    final_decisions = make_final_decisions(
        job_description,
        deep_results
    )

    state["final_decisions"] = final_decisions

    return state


def human_feedback_node(
    state: AgentState
) -> AgentState:
    """
    Store recruiter feedback for future refinement.
    """

    print("[Node] Human Feedback")

    feedback = state.get(
        "human_feedback",
        ""
    )

    if feedback:
        print(
            f"Recruiter feedback: {feedback}"
        )

    return state

def apply_feedback_node(
    state: AgentState
) -> AgentState:
    """
    Apply recruiter feedback to the job description
    so candidates can be re-ranked.
    """

    print("[Node] Apply Feedback")

    feedback = state.get(
        "human_feedback",
        ""
    )

    if not feedback:
        return state

    job_description = state.get(
        "job_description",
        ""
    )

    model = ChatOpenRouter(
        model=OPENROUTER_MODEL,
        temperature=0,
    )

    prompt = f"""
You are a recruitment assistant.

The recruiter has provided feedback about
candidate ranking.

Original Job Description:
{job_description}

Recruiter Feedback:
{feedback}

Update the job description so that the
recruiter's preference is reflected.

Rules:
- Keep all original requirements.
- Do not remove existing requirements.
- Add the recruiter preference clearly.
- Do not invent unrelated requirements.

Return ONLY the updated job description.
"""

    response = model.invoke(prompt)

    updated_job_description = response.content.strip()

    state["job_description"] = updated_job_description
    state["feedback_applied"] = True

    print(
        "Updated job description based on feedback."
    )

    return state

def route_after_feedback(state: AgentState) -> str:

    feedback = state.get(
        "human_feedback",
        ""
    ).strip()

    feedback_applied = state.get(
        "feedback_applied",
        False
    )

    if feedback and not feedback_applied:
        return "apply_feedback"

    return "deep_screening"


# --------------------------------------------------
# Build LangGraph
# --------------------------------------------------

def build_matching_agent():

    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node(
        "parse_jd",
        parse_jd
    )

    graph.add_node(
        "extract_requirements",
        extract_requirements_node
    )

    graph.add_node(
        "search_resumes",
        search_resumes_node
    )

    graph.add_node(
        "rank_candidates",
        rank_candidates_node
    )

    graph.add_node(
        "generate_report",
        generate_report_node
    )

    graph.add_node(
        "human_feedback",
        human_feedback_node
    )

    graph.add_node(
        "apply_feedback",
        apply_feedback_node
    )

    graph.add_node(
        "deep_screening",
        deep_screening_node
    )

    graph.add_node(
        "final_decision",
        final_decision_node
    )

    # --------------------------------------------------
    # Define workflow
    # --------------------------------------------------

    graph.add_edge(
        START,
        "parse_jd"
    )

    graph.add_edge(
        "parse_jd",
        "extract_requirements"
    )

    graph.add_edge(
        "extract_requirements",
        "search_resumes"
    )

    graph.add_edge(
        "search_resumes",
        "rank_candidates"
    )

    graph.add_edge(
        "rank_candidates",
        "generate_report"
    )

    graph.add_edge(
        "generate_report",
        "human_feedback"
    )

    graph.add_conditional_edges(
        "human_feedback",
        route_after_feedback,
        {
            "apply_feedback": "apply_feedback",
            "deep_screening": "deep_screening"
        }
    )

    graph.add_edge(
        "deep_screening",
        "final_decision"
    )

    graph.add_edge(
        "final_decision",
        END
    )

    graph.add_edge(
        "apply_feedback",
        "extract_requirements"
    )

    return graph.compile()


# --------------------------------------------------
# Create agent
# --------------------------------------------------

matching_agent = build_matching_agent()