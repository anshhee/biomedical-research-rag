import { AskRequest, AskResponse } from "@/types/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) {
  // Only warn at module load time — the variable must be set before running.
  console.warn(
    "[api] NEXT_PUBLIC_API_URL is not set. Requests will fail. " +
      "Create a .env.local file with NEXT_PUBLIC_API_URL=http://127.0.0.1:8000"
  );
}

/**
 * Sends a question to the FastAPI POST /ask endpoint and returns the response.
 * Throws an Error with a user-friendly message on any failure.
 */
export async function askQuestion(request: AskRequest): Promise<AskResponse> {
  const endpoint = `${API_URL}/ask`;

  let response: Response;

  try {
    response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
  } catch (networkError) {
    throw new Error(
      "Unable to reach the RAG service. Please ensure the backend is running and accessible."
    );
  }

  if (!response.ok) {
    // Try to extract a detail message from the JSON response body.
    let detail = `Request failed with status ${response.status}.`;
    try {
      const errorBody = await response.json();
      if (errorBody?.detail) {
        // Map known HTTP status codes to friendlier messages.
        if (response.status === 503) {
          detail =
            "The RAG service is temporarily unavailable. Please try again shortly.";
        } else if (response.status === 422) {
          detail = "Invalid request. Please check your question and try again.";
        } else {
          detail = String(errorBody.detail);
        }
      }
    } catch {
      // Ignore JSON parse errors; use the default detail message.
    }
    throw new Error(detail);
  }

  const data: AskResponse = await response.json();
  return data;
}
