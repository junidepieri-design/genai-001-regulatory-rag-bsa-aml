# generation.py
# Builds the LLM and generates answers grounded in retrieved context.

from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE


def build_llm():
    '''
    Initializes the Gemini LLM with temperature zero.
    Temperature is fixed at 0.0 for deterministic compliance answers.
    '''
    
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=LLM_TEMPERATURE
    )


def generate_answer(user_query, retrieved_chunks, llm):
    '''
    Builds a prompt from retrieved chunks and generates a cited answer.
    Every claim in the answer must reference its source page number.
    Returns not found message if context is insufficient.
    '''

    # Build context with page references
    context_blocks = ""
    for chunk in retrieved_chunks:
        source_page = chunk.metadata.get("page", "?")
        context_blocks += f"[Page {source_page}]\n{chunk.page_content}\n\n"

    prompt = f"""
        You are a BSA/AML compliance expert assistant.
        Answer the question based ONLY on the context provided.
        Always cite the source page number for every claim.
        If the answer is not in the context, say "Not found in the document."

        Context:
        {context_blocks}

        Question: {user_query}

        Answer (always cite page numbers):
    """

    llm_response = llm.invoke(prompt)
    return llm_response.content