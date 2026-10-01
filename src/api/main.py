from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.api.schemas import AskRequest, AskResponse
from src.rag.service import generate_answer
from src.api.exceptions import RAGServiceError 

app = FastAPI()

# CORS — allow the Next.js frontend (localhost:3000) to call this API.
# Only CORSMiddleware is added; no RAG or API logic is changed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


@app.post("/ask", response_model=AskResponse)


def ask(request: AskRequest):
    try:

        result = generate_answer(
        query=request.question,
        k=5
    )

    except RAGServiceError:
        raise HTTPException(
            status_code=503,
            detail="RAG service is temporarily unavailable."
        )


    sources = [
        {
            "doc_id": chunk["doc_id"],
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
            "text": chunk["text"]
        }
        for chunk in result["chunks"]
    ]

    return {
        "status": "answered",
        "answer": result["answer"],
        "sources": sources
    }