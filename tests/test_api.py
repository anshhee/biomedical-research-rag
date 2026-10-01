from fastapi.testclient import TestClient

from src.api.main import app
from src.api.exceptions import RAGServiceError


client = TestClient(app)


def test_ask_endpoint():
    response = client.post(
        "/ask",
        json={
            "question": "What is PSMA-targeted radioligand therapy?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "status" in data
    assert "sources" in data

    assert data["status"] == "answered"
    assert isinstance(data["answer"], str)
    assert isinstance(data["sources"], list)

    for source in data["sources"]:

        assert "doc_id" in source
        assert "chunk_id" in source
        assert "source" in source
        assert "text" in source


def test_ask_service_failure(monkeypatch):
    def mock_generate_answer(query, k):
        raise RAGServiceError("RAG service failed.")

    monkeypatch.setattr(
        "src.api.main.generate_answer",
        mock_generate_answer
    )

    response = client.post(
        "/ask",
        json={
            "question": "What is PSMA-targeted radioligand therapy?"
        }
    )

    assert response.status_code == 503

    data = response.json()

    assert data["detail"] == "RAG service is temporarily unavailable."


def test_ask_validation_error():
    response = client.post(
        "/ask",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422