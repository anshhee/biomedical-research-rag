from fastapi import FastAPI, HTTPException
from src.api.schemas import AskRequest, AskResponse
from src.rag.service import generate_answer
from src.api.exceptions import RAGServiceError 

app = FastAPI()


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