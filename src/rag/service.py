import json
from pathlib import Path

import chromadb
import ollama
from src.api.exceptions import RAGServiceError

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma"


# Load chunk metadata once when the service starts
with open(
    PROCESSED_DIR / "chunked_documents.json",
    "r",
    encoding="utf-8"
) as f:
    chunked_documents = json.load(f)


# Create lookup for fast chunk retrieval
chunk_lookup = {
    chunk["chunk_id"]: chunk
    for chunk in chunked_documents
}


# Connect to existing Chroma database
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="documents"
)


def retrieve_chunks(query: str, k: int = 5):
    """Retrieve the top-k chunks for a query."""

    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=query
    )

    query_embedding = response["embedding"]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    chunk_ids = results["ids"][0]

    return [
        chunk_lookup[chunk_id]
        for chunk_id in chunk_ids
    ]



def generate_answer(
    query: str,
    k: int = 5,
    model: str = "qwen2.5:3b"
):
    try:
        retrieved_chunks = retrieve_chunks(
            query=query,
            k=k
        )

        context = "\n\n".join(
            [
                f"[Source {i}]\n{chunk['text']}"
                for i, chunk in enumerate(
                    retrieved_chunks,
                    start=1
                )
            ]
        )

        prompt = f"""
You are answering a biomedical research question using retrieved evidence.

Question:
{query}

Retrieved evidence:
{context}

Instructions:
- Answer the question using only the retrieved evidence.
- Do not introduce facts that are not supported by the evidence.
- If the evidence is insufficient for a claim, say so.
- Give a concise, factual answer.
"""

        response = ollama.generate(
            model="qwen2.5:3b", 
            prompt=prompt
        )

        return {
            "answer": response["response"],
            "chunks": retrieved_chunks
        }

    except Exception as exc:
        raise RAGServiceError(
            "RAG service failed."
        ) from exc