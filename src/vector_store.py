import chromadb
from pathlib import Path


class ResumeVectorStore:

    def __init__(self, persist_directory="chroma_db"):

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name="resume_chunks"
        )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
        resume_path: str,
        metadata: dict
    ):
        """
        Store resume chunks, embeddings, and metadata in ChromaDB.
        """

        documents = []
        metadatas = []
        ids = []

        resume_id = Path(resume_path).stem

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            chunk_id = f"{resume_id}_chunk_{index}"

            documents.append(chunk["text"])

            metadatas.append({
                "candidate_name": metadata["candidate_name"],
                "resume_path": resume_path,
                "section": chunk["section"],
                "skills": ", ".join(metadata["skills"]),
                "experience_years": metadata["experience_years"],
                "education": metadata["education"]
            })

            ids.append(chunk_id)

        self.collection.upsert(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 10
    ):

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

    def count(self):

        return self.collection.count()