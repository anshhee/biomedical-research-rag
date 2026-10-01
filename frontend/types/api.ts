// Types matching the existing FastAPI backend API contract exactly.
// DO NOT add or remove fields — the backend schema is fixed.

export type AskRequest = {
  question: string;
};

export type Source = {
  doc_id: string;
  chunk_id: string;
  source: string;
  text: string;
};

export type AskResponse = {
  answer: string;
  status: string;
  sources: Source[];
};
