import src.rag.service as rag_service
from src.api.exceptions import RAGServiceError


def test_generate_answer(monkeypatch):

    fake_chunks = [
        {
            "doc_id": "doc1",
            "chunk_id": "doc1_0",
            "source": "europe_pmc",
            "text": "PSMA-targeted therapy is used in prostate cancer."
        }
    ]

    def mock_retrieve_chunks(query, k):
        return fake_chunks

    def mock_generate(model, prompt):
        return {
            "response": "PSMA-targeted therapy uses a PSMA-directed ligand."
        }

    monkeypatch.setattr(
        rag_service,
        "retrieve_chunks",
        mock_retrieve_chunks
    )

    monkeypatch.setattr(
        rag_service.ollama,
        "generate",
        mock_generate
    )

    result = rag_service.generate_answer(
        query="What is PSMA-targeted therapy?",
        k=5
    )

    assert result["answer"] == (
        "PSMA-targeted therapy uses a PSMA-directed ligand."
    )

    assert result["chunks"] == fake_chunks


def test_generate_answer_failure(monkeypatch):

    def mock_retrieve_chunks(query, k):
        raise RuntimeError("Retrieval failed")

    monkeypatch.setattr(
        rag_service,
        "retrieve_chunks",
        mock_retrieve_chunks
    )

    try:
        rag_service.generate_answer(
            query="What is PSMA-targeted therapy?",
            k=5
        )

        assert False, "Expected RAGServiceError"

    except RAGServiceError as exc:
        assert str(exc) == "RAG service failed."