from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Embedding model loaded successfully")

    def embed_text(self, text: str):
        return self.model.encode(
            text,
            normalize_embeddings=True
        ).tolist()

    def embed_documents(self, documents: list[str]):
        return self.model.encode(
            documents,
            normalize_embeddings=True
        ).tolist()