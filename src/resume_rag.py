from pathlib import Path

from src.fs_tools import load_resumes
from src.chunker import chunk_resume
from src.metadata import extract_metadata
from src.embeddings import EmbeddingModel
from src.vector_store import ResumeVectorStore


class ResumeRAG:

    def __init__(
        self,
        resume_directory="resumes",
        chroma_directory="chroma_db"
    ):
        self.resume_directory = resume_directory

        self.embedding_model = EmbeddingModel()

        self.vector_store = ResumeVectorStore(
            persist_directory=chroma_directory
        )

    def ingest_resume(self, resume: dict):
        """
        Process and store one resume.
        """

        resume_path = resume["filepath"]
        text = resume["text"]

        # Extract metadata
        metadata = extract_metadata(text)

        # Create intelligent chunks
        chunks = chunk_resume(text)

        if not chunks:
            print(
                f"Skipping empty resume: {resume_path}"
            )
            return 0

        # Generate embeddings
        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.embedding_model.embed_documents(
            texts
        )

        # Store in ChromaDB
        self.vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
            resume_path=resume_path,
            metadata=metadata
        )

        print(
            f"✓ {metadata['candidate_name']} "
            f"→ {len(chunks)} chunks"
        )

        return len(chunks)

    def ingest_all_resumes(self):
        """
        Process every resume in the resume directory.
        """

        resumes = load_resumes(
            self.resume_directory
        )

        if not resumes:
            print(
                f"No resumes found in "
                f"{self.resume_directory}"
            )
            return

        print(
            f"\nFound {len(resumes)} resume(s)"
        )

        print("=" * 60)

        total_chunks = 0

        for resume in resumes:

            try:

                chunks = self.ingest_resume(
                    resume
                )

                total_chunks += chunks

            except Exception as e:

                print(
                    f"✗ Failed to process "
                    f"{resume['filepath']}: {e}"
                )

        print("=" * 60)

        print(
            f"Successfully processed "
            f"{len(resumes)} resume(s)"
        )

        print(
            f"Total chunks stored: "
            f"{total_chunks}"
        )

        print(
            f"ChromaDB total chunks: "
            f"{self.vector_store.count()}"
        )

    def search(self, query: str, top_k: int = 10):
        """
        Perform semantic search against resumes.
        """

        query_embedding = (
            self.embedding_model.embed_text(query)
        )

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )