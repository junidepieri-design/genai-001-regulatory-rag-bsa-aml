# config.py
# Central configuration file for the BSA/AML RAG pipeline.
# All parameters are defined here — no hardcoded values elsewhere.

import os
from dotenv import load_dotenv

load_dotenv()

# API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# PDF Source
PDF_PATH = os.path.abspath('../data/BsaAmlManualSectionsPackage.pdf')

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Vector Store
COLLECTION_NAME = 'bsa_aml'

# Embedding
EMBEDDING_MODEL = 'models/gemini-embedding-001'

# LLM
LLM_MODEL = 'models/gemini-2.5-flash-lite'
LLM_TEMPERATURE = 0.0

# Retrieval
TOP_K = 5