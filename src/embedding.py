# embedding.py
# Generates embeddings and indexes chunks into ChromaDB.

import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GOOGLE_API_KEY, EMBEDDING_MODEL, COLLECTION_NAME


def build_vector_store(document_chunks):
    '''
    Generates embeddings for all chunks using Gemini.
    Indexes them into a local ChromaDB collection.
    Returns the collection and embedding model for retrieval.
    '''
    embedding_model = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY
    )

    chroma_client = chromadb.Client()
    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)

    chunk_texts = [chunk.page_content for chunk in document_chunks]
    chunk_metadatas = [chunk.metadata for chunk in document_chunks]
    chunk_ids = [str(chunk.metadata["chunk_id"]) for chunk in document_chunks]
    chunk_embeddings = embedding_model.embed_documents(chunk_texts)

    chroma_collection.add(
        documents=chunk_texts,
        metadatas=chunk_metadatas,
        ids=chunk_ids,
        embeddings=chunk_embeddings
    )

    print(f"{chroma_collection.count()} vectors indexed in ChromaDB")
    return chroma_collection, embedding_model