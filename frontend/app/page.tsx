"use client";

import { useState } from "react";
import { QuestionInput } from "@/components/QuestionInput";
import { Answer } from "@/components/Answer";
import { Sources } from "@/components/Sources";
import { askQuestion } from "@/lib/api";
import { AskResponse } from "@/types/api";

type AppState =
  | { phase: "idle" }
  | { phase: "loading" }
  | { phase: "result"; data: AskResponse }
  | { phase: "error"; message: string };

const EXAMPLE_QUESTIONS = [
  "What is PSMA-targeted radioligand therapy?",
  "What are the clinical outcomes of lutetium-177 PSMA in metastatic prostate cancer?",
  "How does PSMA expression affect radioligand therapy eligibility?",
  "What dosimetry considerations are important for PSMA RLT?",
];

export default function Home() {
  const [question, setQuestion] = useState("");
  const [appState, setAppState] = useState<AppState>({ phase: "idle" });

  async function handleSubmit() {
    const trimmed = question.trim();
    if (!trimmed) return;

    setAppState({ phase: "loading" });

    try {
      const response = await askQuestion({ question: trimmed });
      setAppState({ phase: "result", data: response });
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "An unexpected error occurred. Please try again.";
      setAppState({ phase: "error", message });
    }
  }

  function handleExampleClick(q: string) {
    setQuestion(q);
    // Scroll to input.
    document.getElementById("question-textarea")?.focus();
  }

  return (
    <div className="page-wrapper">
      {/* ── Header ── */}
      <header className="site-header" role="banner">
        <div className="header-inner">
          <div className="header-logo" aria-hidden="true">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18" />
            </svg>
          </div>

          <div className="header-text">
            <h1 className="site-title">BioMed RAG</h1>
            <p className="site-description">
              Biomedical Research Intelligence — Prostate Cancer &amp; PSMA
              Radioligand Therapy
            </p>
          </div>

          <div className="header-badge" aria-label="Powered by RAG">
            <span className="badge-dot" aria-hidden="true" />
            RAG-Powered
          </div>
        </div>
      </header>

      <main className="main-content" role="main" id="main">
        {/* ── Question Input ── */}
        <section
          className="input-section"
          aria-label="Research question input"
        >
          <QuestionInput
            value={question}
            onChange={setQuestion}
            onSubmit={handleSubmit}
            isLoading={appState.phase === "loading"}
          />
        </section>

        {/* ── Loading state ── */}
        {appState.phase === "loading" && (
          <div
            className="loading-container"
            role="status"
            aria-live="polite"
            aria-label="Processing your question"
          >
            <div className="loading-card">
              <div className="loading-spinner-large" aria-hidden="true">
                <span />
                <span />
                <span />
              </div>
              <div className="loading-text">
                <p className="loading-title">Retrieving Evidence</p>
                <p className="loading-subtitle">
                  Searching the biomedical corpus and generating an answer…
                </p>
              </div>
            </div>
          </div>
        )}

        {/* ── Error state ── */}
        {appState.phase === "error" && (
          <div
            className="error-container"
            role="alert"
            aria-live="assertive"
            aria-label="Error"
          >
            <div className="error-card">
              <div className="error-icon" aria-hidden="true">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
              </div>
              <div className="error-body">
                <p className="error-title">Something went wrong</p>
                <p className="error-message">{appState.message}</p>
              </div>
              <button
                className="error-dismiss"
                onClick={() => setAppState({ phase: "idle" })}
                aria-label="Dismiss error"
              >
                Try again
              </button>
            </div>
          </div>
        )}

        {/* ── Result state ── */}
        {appState.phase === "result" && (
          <div className="results-container" aria-label="Query results">
            <Answer answer={appState.data.answer} />
            <Sources sources={appState.data.sources} />
          </div>
        )}

        {/* ── Empty / idle state ── */}
        {appState.phase === "idle" && (
          <div className="empty-state" aria-label="Getting started">
            <div className="empty-state-inner">
              <div className="empty-icon" aria-hidden="true">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="11" cy="11" r="8" />
                  <line x1="21" y1="21" x2="16.65" y2="16.65" />
                </svg>
              </div>

              <h2 className="empty-title">
                Ask anything about PSMA radioligand therapy
              </h2>

              <p className="empty-description">
                This assistant retrieves evidence from a curated corpus of
                biomedical literature and clinical-trial records, then generates
                a grounded answer using a local language model.
              </p>

              <div className="capabilities-grid" aria-label="Capabilities">
                <div className="capability-card">
                  <div className="capability-icon" aria-hidden="true">🔬</div>
                  <h3 className="capability-title">Literature Retrieval</h3>
                  <p className="capability-desc">
                    Searches indexed PubMed abstracts and research papers.
                  </p>
                </div>

                <div className="capability-card">
                  <div className="capability-icon" aria-hidden="true">🏥</div>
                  <h3 className="capability-title">Clinical Trials</h3>
                  <p className="capability-desc">
                    Covers ClinicalTrials.gov records for prostate cancer RLT.
                  </p>
                </div>

                <div className="capability-card">
                  <div className="capability-icon" aria-hidden="true">🤖</div>
                  <h3 className="capability-title">AI-Generated Answers</h3>
                  <p className="capability-desc">
                    Answers grounded in retrieved evidence via Qwen LLM.
                  </p>
                </div>

                <div className="capability-card">
                  <div className="capability-icon" aria-hidden="true">📄</div>
                  <h3 className="capability-title">Source Transparency</h3>
                  <p className="capability-desc">
                    Every answer includes the retrieved source chunks.
                  </p>
                </div>
              </div>

              <div className="example-questions" aria-label="Example questions">
                <p className="example-label">Try an example:</p>
                <div className="example-chips" role="list">
                  {EXAMPLE_QUESTIONS.map((q) => (
                    <button
                      key={q}
                      role="listitem"
                      className="example-chip"
                      onClick={() => handleExampleClick(q)}
                      aria-label={`Use example question: ${q}`}
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="site-footer" role="contentinfo">
        <p className="footer-text">
          Biomedical Research RAG · Evidence retrieved from PubMed &amp;
          ClinicalTrials.gov · Generated locally by Qwen 2.5
        </p>
      </footer>
    </div>
  );
}
