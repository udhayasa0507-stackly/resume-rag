import pytest

from src.matching_agent import matching_agent
from src.agent_tools import (
    extract_requirements,
    compare_candidates,
    generate_interview_questions,
)
from deep_screening import deep_screen_candidates
from final_decision import make_final_decisions


AI_ENGINEER_JD = """
AI Engineer

We are looking for an AI engineer with 3+ years of experience.

Must-have requirements:
- Python
- Machine Learning
- Deep Learning
- PyTorch
- LLM
- FastAPI

Experience building AI-powered applications is preferred.
"""


def test_agent_compiles():
    """Verify the LangGraph agent was successfully built."""

    assert matching_agent is not None


def test_extract_requirements():
    """Verify JD requirements can be extracted."""

    requirements = extract_requirements(
        AI_ENGINEER_JD
    )

    assert requirements is not None
    assert len(str(requirements)) > 0


def test_agent_ranking():
    """Verify the complete ranking workflow."""

    state = {
        "conversation_history": [],
        "job_description": AI_ENGINEER_JD,
        "human_feedback": "",
        "feedback_applied": False,
    }

    result = matching_agent.invoke(state)

    assert "ranking_results" in result
    assert len(result["ranking_results"]) > 0

    for candidate in result["ranking_results"]:

        assert "candidate_name" in candidate
        assert "match_score" in candidate
        assert "matched_skills" in candidate
        assert "reasoning" in candidate


def test_compare_candidates():
    """Verify head-to-head candidate comparison."""

    results = compare_candidates(
        [
            "Aakash Reddy",
            "Neha Singh"
        ],
        AI_ENGINEER_JD
    )

    assert isinstance(results, list)
    assert len(results) > 0

    for candidate in results:

        assert "candidate_name" in candidate
        assert "match_score" in candidate


def test_interview_questions():
    """Verify interview question generation."""

    questions = generate_interview_questions(
        "Aakash Reddy",
        AI_ENGINEER_JD
    )

    assert questions is not None
    assert len(questions) > 0


def test_deep_screening():
    """Verify Round 2 deep candidate screening."""

    state = {
        "conversation_history": [],
        "job_description": AI_ENGINEER_JD,
        "human_feedback": "",
        "feedback_applied": False,
    }

    result = matching_agent.invoke(state)

    candidates = result.get(
        "ranking_results",
        []
    )

    deep_results = deep_screen_candidates(
        AI_ENGINEER_JD,
        candidates[:3]
    )

    assert isinstance(deep_results, list)
    assert len(deep_results) > 0

    for candidate in deep_results:

        assert "candidate_name" in candidate
        assert "initial_match_score" in candidate
        assert "deep_analysis" in candidate


def test_final_decision():
    """Verify Round 3 final HIRE / NO HIRE decisions."""

    state = {
        "conversation_history": [],
        "job_description": AI_ENGINEER_JD,
        "human_feedback": "",
        "feedback_applied": False,
    }

    result = matching_agent.invoke(state)

    deep_results = result.get(
        "deep_screening_results",
        []
    )

    decisions = make_final_decisions(
        AI_ENGINEER_JD,
        deep_results
    )

    assert isinstance(decisions, list)
    assert len(decisions) > 0

    for decision in decisions:

        assert "candidate_name" in decision
        assert "final_decision" in decision
        assert decision["final_decision"] in {
            "HIRE",
            "NO HIRE"
        }


def test_feedback_reranking():
    """Verify recruiter feedback triggers re-ranking."""

    initial_state = {
        "conversation_history": [],
        "job_description": AI_ENGINEER_JD,
        "human_feedback": "",
        "feedback_applied": False,
    }

    initial_result = matching_agent.invoke(
        initial_state
    )

    initial_ranking = initial_result.get(
        "ranking_results",
        []
    )

    feedback_state = {
        "conversation_history": [],
        "job_description": AI_ENGINEER_JD,
        "human_feedback": (
            "Prioritize candidates with "
            "strong PyTorch experience"
        ),
        "feedback_applied": False,
        "ranking_results": initial_ranking,
        "previous_ranking_results": initial_ranking,
    }

    updated_result = matching_agent.invoke(
        feedback_state
    )

    updated_ranking = updated_result.get(
        "ranking_results",
        []
    )

    assert len(updated_ranking) > 0

    assert updated_result.get(
        "feedback_applied"
    ) is True

    assert (
        "ranking_changes"
        in updated_result
    )