"use client";

import React, { useRef, useEffect } from "react";

interface QuestionInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
}

const MAX_CHARS = 2000;

export function QuestionInput({
  value,
  onChange,
  onSubmit,
  isLoading,
}: QuestionInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea height.
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${el.scrollHeight}px`;
  }, [value]);

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      if (!isLoading && value.trim().length > 0) {
        onSubmit();
      }
    }
  }

  const charsLeft = MAX_CHARS - value.length;
  const isOverLimit = charsLeft < 0;
  const canSubmit = !isLoading && value.trim().length > 0 && !isOverLimit;

  return (
    <div className="question-input-card">
      <label htmlFor="question-textarea" className="question-label">
        Ask a Research Question
      </label>

      <div className="textarea-wrapper">
        <textarea
          ref={textareaRef}
          id="question-textarea"
          className={`question-textarea${isOverLimit ? " over-limit" : ""}`}
          placeholder="e.g. What is PSMA-targeted radioligand therapy and what are its clinical outcomes in metastatic prostate cancer?"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          maxLength={MAX_CHARS + 100} /* allow slight overflow for UX */
          disabled={isLoading}
          rows={4}
          aria-label="Research question"
          aria-describedby="char-counter submit-hint"
        />

        <div className="textarea-footer">
          <span
            id="char-counter"
            className={`char-counter${isOverLimit ? " over-limit" : charsLeft < 100 ? " warning" : ""}`}
            aria-live="polite"
          >
            {isOverLimit
              ? `${Math.abs(charsLeft)} characters over limit`
              : `${charsLeft} characters remaining`}
          </span>

          <span id="submit-hint" className="submit-hint">
            Ctrl + Enter to submit
          </span>
        </div>
      </div>

      <button
        id="ask-button"
        className="ask-button"
        onClick={onSubmit}
        disabled={!canSubmit}
        aria-label={isLoading ? "Processing your question…" : "Submit question"}
        aria-busy={isLoading}
      >
        {isLoading ? (
          <>
            <span className="spinner" aria-hidden="true" />
            Analyzing…
          </>
        ) : (
          <>
            <svg
              className="ask-icon"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
            Ask
          </>
        )}
      </button>
    </div>
  );
}


