import json
from typing import List, Dict, Any

from langchain_openrouter import ChatOpenRouter
from src.config import OPENROUTER_MODEL


def parse_llm_json(content: str) -> dict:
    """
    Convert LLM JSON response into a Python dictionary.
    Handles ```json ... ``` responses.
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


def make_final_decisions(
    job_description: str,
    deep_screening_results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Make final HIRE / NO HIRE decisions
    after deep candidate screening.
    """

    model = ChatOpenRouter(
        model=OPENROUTER_MODEL,
        temperature=0,
    )

    final_decisions = []

    for candidate in deep_screening_results:

        candidate_name = candidate.get(
            "candidate_name",
            "Unknown"
        )

        initial_score = candidate.get(
            "initial_match_score",
            0
        )

        deep_analysis = candidate.get(
            "deep_analysis",
            {}
        )

        prompt = f"""
You are the final decision-maker for technical recruitment.

JOB DESCRIPTION:
{job_description}

CANDIDATE:
{candidate_name}

INITIAL MATCH SCORE:
{initial_score}

DEEP SCREENING:
{deep_analysis}

Make a final hiring decision.

Return ONLY valid JSON:

{{
    "candidate_name": "",
    "final_decision": "",
    "final_score": 0,
    "reason": "",
    "key_strengths": [],
    "key_gaps": []
}}

Rules:

- final_decision MUST be exactly one of:
  "HIRE"
  "NO HIRE"

- final_score must be between 0 and 100.
- Use only information provided above.
- Do not invent skills or experience.
- Consider both initial match score and deep screening.
- A candidate with important missing must-have skills
  should generally receive NO HIRE.
- Explain the decision clearly.
"""

        response = model.invoke(prompt)

        try:
            decision = parse_llm_json(
                response.content
            )

        except json.JSONDecodeError:

            decision = {
                "candidate_name": candidate_name,
                "final_decision": "NO HIRE",
                "final_score": 0,
                "reason": "LLM returned invalid JSON.",
                "key_strengths": [],
                "key_gaps": []
            }

        final_decisions.append(decision)

    return final_decisions