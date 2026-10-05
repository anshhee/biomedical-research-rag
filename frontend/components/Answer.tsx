"use client";

import ReactMarkdown from "react-markdown";

interface AnswerProps {
  answer: string;
}

export function Answer({ answer }: AnswerProps) {
  return (
    <section className="answer-section" aria-label="Answer">
      <div className="section-header">
        <div className="section-badge answer-badge" aria-hidden="true">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        </div>
        <h2 className="section-title">Answer</h2>
      </div>

      <div className="answer-card" role="article">
        <div className="answer-text answer-markdown">
          <ReactMarkdown>{answer}</ReactMarkdown>
        </div>
      </div>
    </section>
  );
}
