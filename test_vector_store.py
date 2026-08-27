from src.fs_tools import read_file
from src.chunker import chunk_resume
from src.embeddings import EmbeddingModel
from src.vector_store import ResumeVectorStore
from src.metadata import extract_metadata


# --------------------------------------------------
# 1. Read resume
# --------------------------------------------------

resume_path = "resumes/test_resume.txt"

result = read_file(resume_path)

if not result["success"]:
    print("Error:", result["error"])
    exit()


text = result["text"]


# --------------------------------------------------
# 2. Extract metadata
# --------------------------------------------------

metadata = extract_metadata(text)

print("\nCandidate:", metadata["candidate_name"])
print("Skills:", metadata["skills"])
print("Experience:", metadata["experience_years"])
print("Education:", metadata["education"])


# --------------------------------------------------
# 3. Chunk resume
# --------------------------------------------------

chunks = chunk_resume(text)

print("\nChunks created:", len(chunks))


# --------------------------------------------------
# 4. Generate embeddings
# --------------------------------------------------

embedding_model = EmbeddingModel()

texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = embedding_model.embed_documents(texts)

print("Embeddings generated:", len(embeddings))


# --------------------------------------------------
# 5. Create vector store
# --------------------------------------------------

vector_store = ResumeVectorStore(
    persist_directory="chroma_db"
)


# --------------------------------------------------
# 6. Store resume
# --------------------------------------------------

vector_store.add_chunks(
    chunks=chunks,
    embeddings=embeddings,
    resume_path=resume_path,
    metadata=metadata
)

print("\nResume stored successfully")

print(
    "Total chunks in ChromaDB:",
    vector_store.count()
)


# --------------------------------------------------
# 7. Semantic search
# --------------------------------------------------

query = """
Python backend developer with 5 years
experience using FastAPI and PostgreSQL
"""

query_embedding = embedding_model.embed_text(query)

results = vector_store.search(
    query_embedding=query_embedding,
    top_k=3
)


print("\nSemantic Search Results")
print("=" * 60)


for index, document in enumerate(
    results["documents"][0],
    start=1
):

    result_metadata = results["metadatas"][0][index - 1]

    print(f"\nResult {index}")

    print(
        "Candidate:",
        result_metadata["candidate_name"]
    )

    print(
        "Section:",
        result_metadata["section"]
    )

    print(
        "Skills:",
        result_metadata["skills"]
    )

    print(
        "Experience:",
        result_metadata["experience_years"]
    )

    print(
        "Education:",
        result_metadata["education"]
    )

    print(
        "Text:",
        document
    )