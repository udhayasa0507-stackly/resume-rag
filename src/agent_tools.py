from typing import List, Dict, Any

from src.resume_rag import ResumeRAG
from src.config import OPENROUTER_MODEL
from langchain_openrouter import ChatOpenRouter


# Create one RAG system instance
rag = ResumeRAG()


def rag_search_tool(
    query: str,
    top_k: int = 10
) -> List[Dict[str, Any]]:
    """
    Search resumes using the existing RAG system.
    """

    results = rag.search(
        query=query,
        top_k=top_k
    )

    return results


def extract_requirements(jd: str) -> dict:
    """
    Extract must-have and nice-to-have requirements
    from a job description using an LLM.
    """

    model = ChatOpenRouter(
        model=OPENROUTER_MODEL,
        temperature=0,
    )

    prompt = f"""
You are a recruitment requirements extraction assistant.

Analyze the following job description and extract:

1. Role
2. Must-have skills
3. Nice-to-have skills
4. Required experience
5. Education requirements

Return ONLY valid JSON in this format:

{{
    "role": "",
    "must_have": [],
    "nice_to_have": [],
    "experience": "",
    "education": ""
}}

Job Description:
{jd}
"""

    response = model.invoke(prompt)

    return response.content

from src.job_matcher import JobMatcher


def compare_candidates(
    candidate_ids: list[str],
    job_description: str
) -> list[dict]:
    """
    Compare selected candidates against a job description.

    Args:
        candidate_ids: Candidate names to compare.
        job_description: Current job description.

    Returns:
        Comparison results for the selected candidates.
    """

    # Create the existing job matcher
    matcher = JobMatcher(rag)

    # Run the existing matching system
    match_result = matcher.match_job(
        job_description=job_description,
        top_k=10
    )

    top_matches = match_result["top_matches"]

    # Keep only the requested candidates
    candidate_ids_lower = {
        candidate_id.lower().strip()
        for candidate_id in candidate_ids
    }

    comparison = []

    for candidate in top_matches:

        candidate_name = candidate[
            "candidate_name"
        ]

        if candidate_name.lower().strip() in candidate_ids_lower:

            comparison.append({
                "candidate_name": candidate_name,
                "match_score": candidate[
                    "match_score"
                ],
                "matched_skills": candidate[
                    "matched_skills"
                ],
                "relevant_excerpts": candidate[
                    "relevant_excerpts"
                ],
                "reasoning": candidate[
                    "reasoning"
                ]
            })

    # Highest match score first
    comparison.sort(
        key=lambda candidate: candidate[
            "match_score"
        ],
        reverse=True
    )

    return comparison

def generate_interview_questions(
    candidate_id: str,
    job_description: str
) -> str:
    """
    Generate customized interview questions for a candidate
    based on their resume and the current job description.

    Args:
        candidate_id: Candidate name.
        job_description: Current job description.

    Returns:
        Generated interview questions.
    """

    # Search the candidate's resume
    search_results = rag.search(
        query=candidate_id,
        top_k=10
    )

    documents = search_results["documents"][0]
    metadatas = search_results["metadatas"][0]

    candidate_resume = []

    for document, metadata in zip(
        documents,
        metadatas
    ):
        candidate_name = metadata.get(
            "candidate_name",
            ""
        )

        if candidate_name.lower().strip() == candidate_id.lower().strip():
            candidate_resume.append(document)

    if not candidate_resume:
        return (
            f"Could not find resume information "
            f"for candidate: {candidate_id}"
        )

    resume_text = "\n\n".join(candidate_resume)

    # Create OpenRouter model
    model = ChatOpenRouter(
        model=OPENROUTER_MODEL,
        temperature=0,
    )

    prompt = f"""
You are an experienced technical recruiter.

Generate customized interview screening questions
for the candidate below.

Candidate:
{candidate_id}

Job Description:
{job_description}

Candidate Resume Information:
{resume_text}

Create 8 interview questions.

Include:
1. Technical questions based on the required skills.
2. Questions about the candidate's actual resume experience.
3. Questions that verify important claims.
4. Questions about gaps or missing requirements.
5. One or two practical/problem-solving questions.

Return the questions as a numbered list.

Do not provide answers.
"""

    response = model.invoke(prompt)

    return response.content