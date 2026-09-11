import json
from typing import List, Dict, Any

from langchain_openrouter import ChatOpenRouter
from src.config import OPENROUTER_MODEL

def parse_llm_json(content: str) -> dict:
    """
    Convert LLM JSON response into a Python dictionary.
    Handles responses wrapped in ```json ... ``` blocks.
    """

    content = content.strip()

    if content.startswith("```"):
        lines = content.splitlines()

        if lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        content = "\n".join(lines).strip()

    return json.loads(content)


def deep_screen_candidates(
    job_description: str,
    candidates: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Perform deep LLM-based screening on shortlisted candidates.
    """

    model = ChatOpenRouter(
        model=OPENROUTER_MODEL,
        temperature=0,
    )

    results = []

    for candidate in candidates:

        candidate_name = candidate.get(
            "candidate_name",
            "Unknown"
        )

        matched_skills = candidate.get(
            "matched_skills",
            []
        )

        excerpts = candidate.get(
            "relevant_excerpts",
            []
        )

        match_score = candidate.get(
            "match_score",
            0
        )

        prompt = f"""
You are an expert technical recruiter.

Perform a deep screening analysis for this candidate.

JOB DESCRIPTION:
{job_description}

CANDIDATE:
{candidate_name}

INITIAL MATCH SCORE:
{match_score}

MATCHED SKILLS:
{matched_skills}

RELEVANT RESUME EXCERPTS:
{excerpts}

Analyze the candidate and return ONLY valid JSON:

{{
    "candidate_name": "",
    "technical_fit": "",
    "experience_relevance": "",
    "strengths": [],
    "gaps": [],
    "concerns": [],
    "recommendation": "",
    "deep_score": 0
}}

Rules:
- Use only information present in the candidate data.
- Do not invent experience or skills.
- deep_score must be between 0 and 100.
- recommendation must be one of:
  "Strong Hire",
  "Hire",
  "Maybe",
  "No Hire"
"""

        response = model.invoke(prompt)

        try:
            deep_analysis = parse_llm_json(
                response.content
            )
        except json.JSONDecodeError:
            deep_analysis = {
                "candidate_name": candidate_name,
                "technical_fit": "Unknown",
                "experience_relevance": "Unknown",
                "strengths": [],
                "gaps": [],
                "concerns": [
                    "LLM returned invalid JSON"
                ],
                "recommendation": "Maybe",
                "deep_score": 0
            }

        results.append({
            "candidate_name": candidate_name,
            "initial_match_score": match_score,
            "deep_analysis": deep_analysis
        })

    return results