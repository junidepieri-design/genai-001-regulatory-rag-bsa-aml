# processing.py
# Splits documents into chunks and attaches metadata for retrieval.

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP


def process_documents(extracted_pages):
    '''
    Splits pages into smaller chunks for embedding.
    Adds a unique chunk_id to each chunk metadata.
    Returns a list of Document chunks.
    '''
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    document_chunks = text_splitter.split_documents(extracted_pages)

    for chunk_index, chunk in enumerate(document_chunks):
        chunk.metadata['chunk_id'] = chunk_index

    print(f'{len(document_chunks)} chunks generated')
    return document_chunks