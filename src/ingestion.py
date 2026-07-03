# ingestion.py
# Loads a PDF document and extracts text content page by page.

import pymupdf as fitz
from langchain_core.documents import Document
from config import PDF_PATH


def load_pdf(pdf_path=PDF_PATH):
    '''
    Opens a PDF file and extracts text from each page.
    Returns a list of Documents with page metadata.
    Skips empty pages automatically.
    '''
    pdf_document = fitz.open(pdf_path)
    extracted_pages = []

    for page_index in range(len(pdf_document)):
        current_page = pdf_document[page_index]
        page_text = current_page.get_text()

        if not page_text.strip():
            continue

        extracted_pages.append(Document(
            page_content=page_text,
            metadata={
                'source': pdf_path,
                'page': page_index + 1
            }
        ))

    print(f'{len(extracted_pages)} pages loaded')
    return extracted_pages