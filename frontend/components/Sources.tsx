"use client";

import { Source } from "@/types/api";

interface SourcesProps {
  sources: Source[];
}

export function Sources({ sources }: SourcesProps) {
  if (sources.length === 0) {
    return (
      <section className="sources-section" aria-label="Sources">
        <div className="section-header">
          <div className="section-badge sources-badge" aria-hidden="true">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
          </div>
          <h2 className="section-title">Retrieved Sources</h2>
        </div>
        <p className="no-sources">No sources were retrieved for this answer.</p>
      </section>
    );
  }

  return (
    <section className="sources-section" aria-label="Retrieved sources">
      <div className="section-header">
        <div className="section-badge sources-badge" aria-hidden="true">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
          </svg>
        </div>
        <h2 className="section-title">Retrieved Sources</h2>
        <span className="sources-count" aria-label={`${sources.length} sources`}>
          {sources.length}
        </span>
      </div>

      <ol className="sources-list" aria-label="Source documents">
        {sources.map((source, index) => (
          <li
            key={`${source.doc_id}-${source.chunk_id}-${index}`}
            className="source-item"
          >
            <div className="source-header">
              <span className="source-index" aria-hidden="true">
                {index + 1}
              </span>

              <div className="source-meta">
                <div className="source-meta-row">
                  <span className="source-type-badge">{source.source}</span>
                </div>

                <div className="source-ids">
                  <span className="meta-label">Document</span>
                  <code className="meta-value">{source.doc_id}</code>
                </div>
              </div>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
