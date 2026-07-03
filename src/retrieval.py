# retrieval.py
# Hybrid search combining semantic similarity and BM25 keyword matching.

from rank_bm25 import BM25Okapi
from config import TOP_K


def build_bm25(document_chunks):
    '''
    Builds a BM25 index from document chunks for keyword search.
    Returns a BM25Okapi object ready for querying.
    '''
    tokenized_chunks = [ chunk.page_content.lower().split() for chunk in document_chunks ]
    return BM25Okapi(tokenized_chunks)


def hybrid_search(query, chroma_collection, embedding_model, bm25_index, document_chunks):
    '''
    Combines semantic search and BM25 keyword search.
    Returns a deduplicated list of the most relevant chunks.
    '''
    # Semantic search
    query_embedding = embedding_model.embed_query(query)
    semantic_results = chroma_collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )
    semantic_ids = set(semantic_results['ids'][0])

    # Keyword search via BM25
    tokenized_query = query.lower().split()
    bm25_scores = bm25_index.get_scores(tokenized_query)
    top_bm25_indexes = sorted(
        range(len(bm25_scores)),
        key=lambda index: bm25_scores[index],
        reverse=True
    )[:TOP_K]
    bm25_ids = set(str(index) for index in top_bm25_indexes)

    # Combine and deduplicate
    combined_ids = semantic_ids.union(bm25_ids)
    retrieved_chunks = [document_chunks[int(chunk_id)] for chunk_id in combined_ids]

    print(f'{len(retrieved_chunks)} chunks retrieved')
    return retrieved_chunks