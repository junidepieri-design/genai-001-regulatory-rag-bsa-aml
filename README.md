# BSA/AML Regulatory RAG
### AI for Fintech | [GENAI-001]

A production-grade retrieval-augmented generation system for querying BSA/AML regulatory documents. Ask questions in plain English and get precise answers with citations down to section and page number.

Built on LangChain, ChromaDB, and Google Gemini. Designed to run locally and extend to any stack via a single configuration file.

![Architecture BSA_AML Regulatory RAG](Architecture%20BSA_AML%20Regulatory%20RAG.png)

---

## What This Solves

Compliance teams spend significant time manually searching BSA/AML documentation — FinCEN guidelines, FFIEC manuals, SAR filing requirements. This system answers regulatory questions instantly, always citing the exact source page so compliance officers can verify.

---

## Project Structure

```
bsa-aml-rag/
├── README.md
├── requirements.txt
├── .env
├── config.py
├── src/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── processing.py
│   ├── embedding.py
│   ├── retrieval.py
│   └── generation.py
├── notebooks/
│   └── quickstart.ipynb
└── data/
    └── BsaAmlManualSectionsPackage.pdf
```

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/junidepieri-design/genai-001-regulatory-rag-bsa-aml.git
cd bsa-aml-rag
```

### 2. Create a virtual environment

```bash
# Windows
py -3.13 -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the .env file

Copy the example file and add your API key.

```bash
cp .env.example .env
```

Open `.env` and fill in your Google AI Studio key:

```
GOOGLE_API_KEY=your_key_here
```

Get your free API key at [aistudio.google.com](https://aistudio.google.com).

### 5. Configure the project

Open `config.py` and adjust the parameters as needed:

```python
PDF_PATH       = path to your regulatory document
CHUNK_SIZE     = size of each text chunk (default: 500)
CHUNK_OVERLAP  = overlap between chunks (default: 50)
EMBEDDING_MODEL = Gemini embedding model to use
LLM_MODEL      = Gemini LLM model to use
LLM_TEMPERATURE = 0.0 for deterministic compliance answers
TOP_K          = number of chunks retrieved per query
```

### 6. Add your document

Place your BSA/AML PDF in the `data/` folder and update `PDF_PATH` in `config.py` accordingly.

The FFIEC BSA/AML Examination Manual is publicly available at [bsaaml.ffiec.gov](https://bsaaml.ffiec.gov/manual).

### 7. Run the notebook

Open `notebooks/quickstart.ipynb` in VSCode or Jupyter and run all cells.

```python
run("What are the internal controls required for BSA/AML compliance?")
```

---

## How It Works

```
PDF Document
     │
     ▼ load_pdf()
Extracted Pages
     │
     ▼ process_documents()
Text Chunks + Metadata (page, source)
     │
     ▼ build_vector_store()
ChromaDB Index + Gemini Embeddings
     │
     ▼ hybrid_search()
Semantic Search + BM25 Keyword Search
     │
     ▼ generate_answer()
Answer + Source + Page Number (T=0.0)
```

---

## Key Design Decisions

**Temperature fixed at 0.0** — Regulatory answers must be deterministic. Creativity is a liability in compliance contexts.

**Hybrid retrieval** — Regulatory documents use precise legal terms. Pure semantic search misses exact matches. BM25 keyword search covers what embeddings miss.

**Mandatory citation** — Every answer references the source page. Compliance officers can verify instantly without trusting the model blindly.

**Pluggable stack** — Swap the LLM, embedding model, or vector store through `config.py`. No code changes required.

---

## Configuration Reference

All parameters live in `config.py` and are loaded from `.env`.

| Parameter | Default | Description |
|-----------|---------|-------------|
| GOOGLE_API_KEY | required | Google AI Studio API key |
| PDF_PATH | data/BsaAmlManualSectionsPackage.pdf | Path to the regulatory document |
| CHUNK_SIZE | 500 | Number of characters per chunk |
| CHUNK_OVERLAP | 50 | Overlap between consecutive chunks |
| COLLECTION_NAME | bsa_aml | ChromaDB collection name |
| EMBEDDING_MODEL | models/gemini-embedding-001 | Gemini embedding model |
| LLM_MODEL | gemini-2.0-flash | Gemini LLM model |
| LLM_TEMPERATURE | 0.0 | Generation temperature |
| TOP_K | 5 | Number of chunks retrieved per query |

---

## What v2 Would Look Like

This project intentionally keeps scope tight for v1. Natural next steps include multi-document support across all FFIEC sections, fine-tuned embeddings for regulatory language, conversational memory for follow-up questions, and production deployment with access controls via Unity Catalog on Databricks.

If your team needs to go beyond this baseline, that is where consulting adds value.

---

## Dataset

This project uses publicly available documents from the FFIEC BSA/AML InfoBase.

[bsaaml.ffiec.gov/manual](https://bsaaml.ffiec.gov/manual)

No proprietary data is required to run the project.

---

## Author

Built by [Odemir Depieri Jr](https://www.linkedin.com/in/odemir-depieri-jr/) — Data and AI specialist focused on production systems for financial institutions.
