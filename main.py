from src.resume_rag import ResumeRAG


def main():

    print("=" * 60)
    print("RESUME RAG SYSTEM")
    print("=" * 60)

    rag = ResumeRAG(
        resume_directory="resumes",
        chroma_directory="chroma_db"
    )

    # Ingest resumes
    rag.ingest_all_resumes()

    # Test semantic search
    query = input(
        "\nEnter a search query: "
    )

    results = rag.search(
        query=query,
        top_k=5
    )

    print("\nSearch Results")
    print("=" * 60)

    if not results["documents"][0]:

        print("No results found.")
        return

    for index, document in enumerate(
        results["documents"][0],
        start=1
    ):

        metadata = results["metadatas"][0][index - 1]

        print(f"\nResult {index}")
        print("-" * 60)

        print(
            "Candidate:",
            metadata["candidate_name"]
        )

        print(
            "Section:",
            metadata["section"]
        )

        print(
            "Skills:",
            metadata["skills"]
        )

        print(
            "Experience:",
            metadata["experience_years"]
        )

        print(
            "Education:",
            metadata["education"]
        )

        print(
            "Excerpt:",
            document
        )


if __name__ == "__main__":
    main()