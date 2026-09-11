from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict, total=False):
    # Conversation between the user and the agent
    conversation_history: List[Dict[str, str]]

    # Original job description provided by the user
    job_description: str

    # Requirements extracted from the job description
    requirements: Dict[str, Any]

    # Candidates retrieved from the RAG system
    candidate_shortlist: List[Dict[str, Any]]

    # Final ranking and reasoning
    ranking_results: List[Dict[str, Any]]

    # Previous ranking before recruiter feedback
    previous_ranking_results: List[Dict[str, Any]]

    # Explanation of how the ranking changed
    ranking_changes: List[Dict[str, Any]]

    # Generated report for the recruiter
    final_report: str

    # Feedback provided by the human/recruiter
    human_feedback: str

    # Tracks whether the current feedback has already been applied
    feedback_applied: bool

    # Candidates selected for deeper screening
    deep_screening_results: List[Dict[str, Any]]

    # Final hiring decisions
    final_decisions: List[Dict[str, Any]]