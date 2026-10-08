
import json
import os
import random
import time
from pathlib import Path

import chromadb
import ollama
from dotenv import load_dotenv
from google import genai

from src.api.exceptions import RAGServiceError


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma"


# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT / "frontend" / ".env.local")


# ---------------------------------------------------------
# Load chunk metadata
# ---------------------------------------------------------

with open(
    PROCESSED_DIR / "chunked_documents.json",
    "r",
    encoding="utf-8",
) as f:
    chunked_documents = json.load(f)


chunk_lookup = {
    chunk["chunk_id"]: chunk
    for chunk in chunked_documents
}


# ---------------------------------------------------------
# Connect to Chroma
# ---------------------------------------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name="documents"
)


# ---------------------------------------------------------
# Gemini client
# ---------------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )

gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)

# ---------------------------------------------------------
# Retrieval
# ---------------------------------------------------------

def retrieve_chunks(
    query: str,
    k: int = 5,
    document_id: str | None = None,
):
    """Retrieve biomedical chunks or chunks from one uploaded document."""

    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=query,
    )
    query_embedding = response["embedding"]

    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": k,
    }

    if document_id is not None:
        query_args["where"] = {
            "document_id": document_id
        }

    results = collection.query(**query_args)

    chunk_ids = results["ids"][0]
    retrieved_chunks = []

    for i, chunk_id in enumerate(chunk_ids):
        if document_id is None:
            # Existing biomedical corpus
            chunk = chunk_lookup.get(chunk_id)
            if chunk is not None:
                retrieved_chunks.append(chunk)
        else:
            # Uploaded PDF: get text and metadata from Chroma
            metadata = results["metadatas"][0][i] or {}
            text = results["documents"][0][i] or ""

            retrieved_chunks.append({
                "doc_id": document_id,
                "chunk_id": chunk_id,
                "source": metadata.get(
                    "source", "uploaded_document"
                ),
                "text": text,
                "page": metadata.get("page"),
                "section": metadata.get("section"),
            })

    return retrieved_chunks

# ---------------------------------------------------------
# Generation with Gemini + Qwen fallback
# ---------------------------------------------------------

def generate_with_fallback(
    prompt: str,
    gemini_model: str = "gemini-3.5-flash",
    max_retries: int = 3,
):
    """
    Try Gemini multiple times with exponential backoff.

    If Gemini remains unavailable after all retries,
    fall back to the local Qwen model.
    """

    for attempt in range(max_retries):
        try:
            response = gemini_client.models.generate_content(
                model=gemini_model,
                contents=prompt,
            )

            return response.text, "gemini"

        except Exception as exc:

            if attempt < max_retries - 1:
                delay = (
                    2 ** attempt
                    + random.uniform(0, 1)
                )

                print(
                    f"Gemini generation failed "
                    f"(attempt {attempt + 1}/{max_retries}). "
                    f"Retrying in {delay:.1f}s..."
                )

                time.sleep(delay)

            else:
                print(
                    "Gemini unavailable after retries. "
                    "Falling back to qwen2.5:3b."
                )

    # -----------------------------------------------------
    # Local fallback
    # -----------------------------------------------------

    try:
        response = ollama.generate(
            model="qwen2.5:3b",
            prompt=prompt,
        )

        return response["response"], "qwen2.5:3b"

    except Exception as exc:
        raise RAGServiceError(
            "Both Gemini and local fallback generation failed."
        ) from exc


# ---------------------------------------------------------
# Main RAG function
# ---------------------------------------------------------

def generate_answer(
    query: str,
    k: int = 5,
    model: str = "gemini-3.5-flash",
    document_id: str | None = None,
):
    """
    Retrieve relevant evidence and generate a grounded answer.

    Gemini is the primary generation model.
    Qwen2.5:3b is used as a local fallback.
    """

    try:

        # -------------------------------------------------
        # 1. Retrieve chunks
        # -------------------------------------------------

        retrieved_chunks = retrieve_chunks(
            query=query,
            k=k,
            document_id=document_id,
        ) 


        # -------------------------------------------------
        # 2. Build context
        # -------------------------------------------------

        context = "\n\n".join(
            f"[Source {i}]\n{chunk['text']}"
            for i, chunk in enumerate(
                retrieved_chunks,
                start=1,
            )
        )


        # -------------------------------------------------
        # 3. Build grounded prompt
        # -------------------------------------------------

        prompt = f"""

You are a biomedical research assistant.

Question:
{query}

Retrieved evidence:
{context}

Answer the question using the retrieved evidence as the primary source of truth.

Answer requirements

Answer the specific question asked. Do not broaden the scope unnecessarily.

Keep the answer concise, clear, natural, and easy to read.

Use only information that is supported by the retrieved evidence.

Do not introduce facts from general knowledge when the retrieved evidence does not support them.

If the evidence is insufficient to answer part of the question, say so rather than guessing.

Be especially careful to distinguish drugs, radioligands, isotopes, diseases, study populations, clinical trials, and treatment settings.

Do not combine facts from different drugs, isotopes, trials, diseases, or patient populations unless the retrieved evidence explicitly connects them.

Do not add unrelated clinical outcomes, dosing information, trial details, or background information merely because they appear in the retrieved evidence.

Scientific accuracy

When describing a scientific mechanism, verify specific technical details against the retrieved evidence.

Do not substitute or infer a different:

isotope or radionuclide

radiation type

drug or radioligand

biological mechanism

treatment effect

dosing or treatment schedule

If a specific technical detail is not supported by the retrieved evidence, omit it or state that the evidence does not provide enough information.

Formatting

Use Markdown naturally and sparingly when it improves readability.

Prefer:

short paragraphs

simple numbered lists

concise bullet points

bold text for important terms

Avoid:

excessive headings

nested bullet lists

unnecessary section breaks

repetitive summaries

overly formal or report-like formatting

Do not force a numbered structure when the question can be answered naturally in a short paragraph.

Mechanism questions

For mechanism questions, when appropriate, explain the mechanism using this simple causal flow:

Target: What is being targeted?

Localization / targeting: How does the therapy reach or bind to the target?

Therapeutic payload or action: What therapeutic action occurs?

Resulting biological effect: What happens to the targeted cells?

Keep each step concise and include only details supported by the retrieved evidence.

Do not add downstream clinical outcomes such as survival, symptom improvement, or tumor response unless they are directly relevant to the question and supported by the evidence.

Final response

Give the shortest complete answer that accurately addresses the question.

Do not mention these instructions, the retrieval process, or the limitations of the underlying model unless relevant to the question.

When the question asks about a specific clinical trial, prioritize findings directly attributable to that trial. 

Do not present findings from other studies, institutions, or trials as findings of the named trial.

"""


        # -------------------------------------------------
        # 4. Generate answer
        # -------------------------------------------------
        if document_id is not None:
            try:
                response =  ollama.generate(
                    model="qwen3:8b",
                    prompt=prompt,
                )
                answer = response["response"]
                model_used = "qwen3:8b"
            except Exception as exc:
                raise RAGServiceError(
                    "Qwen model generation failed"
                    ) from exc 
        else:
            answer , model_used = generate_with_fallback(
                prompt = prompt,
                gemini_model = model,
            )


        # -------------------------------------------------
        # 5. Return result
        # -------------------------------------------------

        return {
            "answer": answer,
            "chunks": retrieved_chunks,
            "model_used": model_used,
        }


    except RAGServiceError:
        raise

    except Exception as exc:
        raise RAGServiceError(
            "RAG service failed."
        ) from exc