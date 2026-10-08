from pathlib import Path
from uuid import uuid4 
import fitz

from src.ingestion.models import Document, DocumentSection


def load_pdf(file_path: str | Path) -> Document:
    """
    Load a PDF while preserving page boundaries.

    Each non-empty PDF page becomes one DocumentSection.
    Page numbers are 1-indexed.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    if file_path.suffix.lower() != ".pdf":
        raise ValueError(
            f"Expected a PDF file, got: {file_path.suffix}"
        )

    sections: list[DocumentSection] = []

    with fitz.open(file_path) as pdf:

        for page_number, page in enumerate(pdf, start=1):

            text = page.get_text().strip()

            if not text:
                continue

            sections.append(
                DocumentSection(
                    heading=f"Page {page_number}",
                    text=text,
                    page=page_number,
                )
            )

    return Document(
        document_id=str(uuid4()),
        title=file_path.stem,
        filename=file_path.name,   
        source=str(file_path),
        file_type="pdf",
        sections=sections,
    )