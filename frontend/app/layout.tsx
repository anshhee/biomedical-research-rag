import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BioMed RAG — Prostate Cancer & PSMA Radioligand Therapy Research",
  description:
    "A biomedical research RAG application that retrieves evidence from PubMed and ClinicalTrials.gov to answer questions about PSMA-targeted radioligand therapy for prostate cancer.",
  keywords: [
    "PSMA",
    "radioligand therapy",
    "prostate cancer",
    "biomedical research",
    "RAG",
    "clinical trials",
  ],
  openGraph: {
    title: "BioMed RAG — Prostate Cancer Research Intelligence",
    description:
      "Evidence-grounded answers from biomedical literature on PSMA radioligand therapy.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
