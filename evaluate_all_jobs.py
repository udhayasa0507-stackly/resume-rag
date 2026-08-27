from pathlib import Path
import json
import time

from src.resume_rag import ResumeRAG
from src.job_matcher import JobMatcher


JOB_DIR = Path("job_descriptions")


def main():

    print("=" * 70)
    print("RESUME RAG - JOB MATCHING EVALUATION")
    print("=" * 70)

    # Load RAG system once
    rag = ResumeRAG(
        resume_directory="resumes",
        chroma_directory="chroma_db"
    )

    matcher = JobMatcher(rag)

    results = []

    job_files = sorted(
        JOB_DIR.glob("*.txt")
    )

    print(
        f"\nFound {len(job_files)} job descriptions\n"
    )

    for job_file in job_files:

        job_description = job_file.read_text(
            encoding="utf-8"
        )

        print("-" * 70)
        print(f"JOB: {job_file.name}")

        start_time = time.perf_counter()

        result = matcher.match_job(
            job_description,
            top_k=10
        )

        end_time = time.perf_counter()

        latency_ms = (
            end_time - start_time
        ) * 1000

        result["job_file"] = (
            job_file.name
        )

        result["latency_ms"] = round(
            latency_ms,
            2
        )

        results.append(result)

        print(
            f"Latency: {latency_ms:.2f} ms"
        )

        print("\nTop Matches:")

        for rank, candidate in enumerate(
            result["top_matches"],
            start=1
        ):

            print(
                f"{rank:2}. "
                f"{candidate['candidate_name']:<20} "
                f"{candidate['match_score']}"
            )

    # Save results
    output_file = Path(
        "evaluation_results.json"
    )

    output_file.write_text(
        json.dumps(
            results,
            indent=2
        ),
        encoding="utf-8"
    )

    print("\n" + "=" * 70)
    print("EVALUATION COMPLETED")
    print("=" * 70)

    print(
        f"Results saved to: {output_file}"
    )


if __name__ == "__main__":
    main()