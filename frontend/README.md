# BioMed RAG — Frontend

A Next.js + TypeScript frontend for the Biomedical Research RAG application focused on prostate cancer / PSMA-targeted radioligand therapy.

This frontend is a **client only** — it communicates with the existing FastAPI backend via `POST /ask` and renders the answer and retrieved sources. All RAG logic, retrieval, and generation remain in the backend.

---

## Quick Start

### 1. Set up the environment variable

```bash
cp .env.local.example .env.local
```

Edit `.env.local` if your backend runs on a different address:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm run dev
```

The app will be available at **http://localhost:3000**.

---

## Running the Backend

From the project root (the directory containing `src/`):

```bash
uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

Both the frontend (`localhost:3000`) and backend (`localhost:8000`) must be running simultaneously.

---

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx       — Root layout, metadata, Google Fonts
│   ├── page.tsx         — Main page (state machine: idle/loading/result/error)
│   └── globals.css      — Design system (CSS custom properties, all styles)
├── components/
│   ├── QuestionInput.tsx — Textarea, char counter, Ask button
│   ├── Answer.tsx        — Answer display (primary content)
│   └── Sources.tsx       — Retrieved source chunks (accordion)
├── lib/
│   └── api.ts            — Thin API client for POST /ask
├── types/
│   └── api.ts            — TypeScript types matching backend schemas
├── .env.local.example    — Environment variable template
└── README.md
```

---

## API Integration

The frontend calls one endpoint:

```
POST ${NEXT_PUBLIC_API_URL}/ask
Content-Type: application/json

{ "question": "..." }
```

Response shape (from the existing backend):

```json
{
  "answer": "...",
  "status": "answered",
  "sources": [
    {
      "doc_id": "...",
      "chunk_id": "...",
      "source": "...",
      "text": "..."
    }
  ]
}
```

No fields are invented or modified.

---

## Type Checking / Build

```bash
# Type-check only
npx tsc --noEmit

# Production build (validates all TypeScript)
npm run build
```

---

## CORS Note

The backend (`src/api/main.py`) required a one-line CORS middleware addition to allow requests from `localhost:3000`. Only `CORSMiddleware` was added — no RAG, retrieval, or generation logic was touched.
