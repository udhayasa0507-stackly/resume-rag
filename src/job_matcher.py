import re
from collections import defaultdict


TECHNICAL_SKILLS = [
    # Programming Languages
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",

    # Backend Technologies
    "django",
    "fastapi",
    "flask",
    "node.js",

    # Frontend Technologies
    "react",
    "angular",

    # Databases
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "sql",

    # Cloud
    "aws",
    "azure",
    "gcp",

    # DevOps
    "docker",
    "kubernetes",
    "terraform",
    "linux",
    "ci/cd",

    # AI / ML
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "llm",

    # Data
    "pandas",
    "numpy",
    "spark",
    "hadoop",
    "airflow",

    # Other
    "git",
]


DOMAIN_PATTERNS = [
    "backend",
    "frontend",
    "full stack",
    "data science",
    "data engineering",
    "devops",
    "cloud",
]


def skill_exists(skill: str, text: str) -> bool:
    """
    Check whether a skill/domain appears as a complete term.
    """

    pattern = (
        r"(?<![a-zA-Z0-9])"
        + re.escape(skill)
        + r"(?![a-zA-Z0-9])"
    )

    return re.search(
        pattern,
        text,
        re.IGNORECASE
    ) is not None


class JobMatcher:

    def __init__(self, rag):
        self.rag = rag

    # --------------------------------------------------
    # Requirement extraction
    # --------------------------------------------------

    def extract_requirements(
        self,
        job_description: str
    ) -> dict:

        required_skills = []

        for skill in TECHNICAL_SKILLS:

            if skill_exists(
                skill,
                job_description
            ):
                required_skills.append(skill)

        required_domains = []

        for domain in DOMAIN_PATTERNS:

            if skill_exists(
                domain,
                job_description
            ):
                required_domains.append(domain)

        minimum_experience_years = 0.0

        patterns = [
            r"(\d+(?:\.\d+)?)\+?\s*years?\s+(?:of\s+)?experience",
            r"minimum\s+(\d+(?:\.\d+)?)\s*years?",
            r"at least\s+(\d+(?:\.\d+)?)\s*years?"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                job_description,
                re.IGNORECASE
            )

            if match:

                minimum_experience_years = float(
                    match.group(1)
                )

                break

        return {
            "required_skills": required_skills,
            "required_domains": required_domains,
            "minimum_experience_years": minimum_experience_years
        }

    # --------------------------------------------------
    # Semantic retrieval
    # --------------------------------------------------

    def semantic_search(
        self,
        job_description: str,
        top_k: int = 10
    ):

        query_embedding = (
            self.rag.embedding_model.embed_text(
                job_description
            )
        )

        return self.rag.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

    # --------------------------------------------------
    # Group chunks by candidate
    # --------------------------------------------------

    def group_candidates(
        self,
        search_results
    ) -> dict:

        candidates = defaultdict(
            lambda: {
                "candidate_name": "",
                "resume_path": "",
                "skills": [],
                "experience_years": 0.0,
                "education": "",
                "sections": [],
                "excerpts": [],
                "distances": []
            }
        )

        documents = search_results["documents"][0]
        metadatas = search_results["metadatas"][0]
        distances = search_results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            candidate_name = metadata[
                "candidate_name"
            ]

            candidate = candidates[
                candidate_name
            ]

            candidate["candidate_name"] = (
                candidate_name
            )

            candidate["resume_path"] = (
                metadata["resume_path"]
            )

            candidate["skills"] = (
                metadata["skills"]
                .split(", ")
            )

            candidate["experience_years"] = (
                float(
                    metadata["experience_years"]
                )
            )

            candidate["education"] = (
                metadata["education"]
            )

            section = metadata["section"]

            if section not in candidate["sections"]:

                candidate["sections"].append(
                    section
                )

            candidate["excerpts"].append({
                "section": section,
                "text": document,
                "distance": distance
            })

            candidate["distances"].append(
                distance
            )

        return dict(candidates)

    # --------------------------------------------------
    # Skill matching
    # --------------------------------------------------

    def calculate_skill_score(
        self,
        required_skills: list[str],
        candidate_skills: list[str]
    ):

        if not required_skills:
            return 100.0, []

        candidate_skills_lower = {
            skill.lower().strip()
            for skill in candidate_skills
        }

        matched_skills = []

        for required_skill in required_skills:

            if required_skill.lower() in candidate_skills_lower:

                matched_skills.append(
                    required_skill
                )

        score = (
            len(matched_skills)
            / len(required_skills)
        ) * 100

        return score, matched_skills

    # --------------------------------------------------
    # Experience matching
    # --------------------------------------------------

    def calculate_experience_score(
        self,
        required_years: float,
        candidate_years: float
    ):

        if required_years <= 0:
            return 100.0

        if candidate_years >= required_years:
            return 100.0

        return (
            candidate_years
            / required_years
        ) * 100

    # --------------------------------------------------
    # Domain matching
    # --------------------------------------------------

    def calculate_domain_score(
        self,
        required_domains: list[str],
        candidate: dict
    ):
        """
        Calculate domain relevance between
        the job description and candidate resume.
        """

        if not required_domains:
            return 100.0

        candidate_text = " ".join(
            excerpt["text"]
            for excerpt in candidate["excerpts"]
        )

        matched_domains = 0

        for domain in required_domains:

            if skill_exists(
                domain,
                candidate_text
            ):
                matched_domains += 1

        return (
            matched_domains
            / len(required_domains)
        ) * 100

    # --------------------------------------------------
    # Semantic score
    # --------------------------------------------------

    def calculate_semantic_score(
        self,
        distances: list[float]
    ):

        if not distances:
            return 0.0

        best_distance = min(distances)

        score = (
            1 - best_distance
        ) * 100

        return max(
            0.0,
            min(100.0, score)
        )

    # --------------------------------------------------
    # Final score
    # --------------------------------------------------

    def calculate_final_score(
        self,
        semantic_score: float,
        skill_score: float,
        experience_score: float,
        domain_score: float
    ):

        final_score = (
            semantic_score * 0.35
            + skill_score * 0.40
            + experience_score * 0.15
            + domain_score * 0.10
        )

        return round(
            final_score,
            2
        )

    # --------------------------------------------------
    # Reasoning
    # --------------------------------------------------

    def generate_reasoning(
        self,
        candidate: dict,
        matched_skills: list[str],
        required_skills: list[str],
        minimum_experience: float
    ):

        candidate_experience = (
            candidate["experience_years"]
        )

        skill_count = len(
            matched_skills
        )

        required_skill_count = len(
            required_skills
        )

        if minimum_experience > 0:

            experience_text = (
                f"{candidate_experience:g} years "
                f"of experience against the required "
                f"{minimum_experience:g}+ years"
            )

        else:

            experience_text = (
                f"{candidate_experience:g} years "
                f"of experience"
            )

        if required_skill_count:

            skill_text = (
                f"matched {skill_count} of "
                f"{required_skill_count} required skills"
            )

        else:

            skill_text = (
                "no specific technical skills "
                "were required"
            )

        sections = ", ".join(
            candidate["sections"]
        )

        return (
            f"Candidate has {experience_text} and "
            f"{skill_text}. Relevant resume sections: "
            f"{sections}."
        )

    # --------------------------------------------------
    # Complete job matching
    # --------------------------------------------------

    def match_job(
        self,
        job_description: str,
        top_k: int = 10
    ):

        requirements = (
            self.extract_requirements(
                job_description
            )
        )

        required_skills = (
            requirements["required_skills"]
        )

        required_domains = (
            requirements["required_domains"]
        )

        minimum_experience = (
            requirements[
                "minimum_experience_years"
            ]
        )

        # Retrieve more chunks than needed
        # because multiple chunks belong
        # to the same candidate.
        search_results = self.semantic_search(
            job_description,
            top_k=max(top_k * 3, 20)
        )

        candidates = self.group_candidates(
            search_results
        )

        ranked_candidates = []

        for candidate in candidates.values():

            # Must-have experience filter
            if (
                minimum_experience > 0
                and candidate["experience_years"]
                < minimum_experience
            ):
                continue

            skill_score, matched_skills = (
                self.calculate_skill_score(
                    required_skills,
                    candidate["skills"]
                )
            )

            # Remove candidates with very little
            # technical skill overlap.
            if (
                required_skills
                and len(matched_skills) < 2
            ):
                continue

            experience_score = (
                self.calculate_experience_score(
                    minimum_experience,
                    candidate["experience_years"]
                )
            )

            domain_score = (
                self.calculate_domain_score(
                    required_domains,
                    candidate
                )
            )

            semantic_score = (
                self.calculate_semantic_score(
                    candidate["distances"]
                )
            )

            final_score = (
                self.calculate_final_score(
                    semantic_score,
                    skill_score,
                    experience_score,
                    domain_score
                )
            )

            reasoning = (
                self.generate_reasoning(
                    candidate,
                    matched_skills,
                    required_skills,
                    minimum_experience
                )
            )

            # Select the 3 most relevant excerpts
            sorted_excerpts = sorted(
                candidate["excerpts"],
                key=lambda item: item["distance"]
            )

            relevant_excerpts = [
                excerpt["text"]
                for excerpt in sorted_excerpts[:3]
            ]

            ranked_candidates.append({
                "candidate_name": candidate[
                    "candidate_name"
                ],
                "resume_path": candidate[
                    "resume_path"
                ],
                "match_score": final_score,
                "matched_skills": matched_skills,
                "relevant_excerpts": relevant_excerpts,
                "reasoning": reasoning
            })

        # Highest score first
        ranked_candidates.sort(
            key=lambda item: item[
                "match_score"
            ],
            reverse=True
        )

        return {
            "job_description": job_description,
            "top_matches": ranked_candidates[
                :top_k
            ]
        }