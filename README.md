# Event Horizon

A retrieval-augmented generation (RAG) system for answering questions about black hole physics, grounded in articles from Quanta Magazine.

## How it works

1. 286 articles from Quanta Magazine are scraped, chunked into 400-token pieces, and embedded using OpenAI's text-embedding-3-small model
2. Embeddings are stored in a PostgreSQL database with the pgvector extension (Neon)
3. When a question is asked, it is embedded and compared against all stored chunks using cosine similarity
4. The top 3 most relevant chunks are retrieved and passed to GPT-4o-mini as context
5. The model generates an answer grounded in the retrieved context, with citations to the source articles

## Stack

- Embeddings: OpenAI text-embedding-3-small (1536 dimensions)
- Vector database: PostgreSQL + pgvector on Neon
- Generation: GPT-4o-mini
- Backend: FastAPI
- Frontend: Streamlit

## Project structure

    fetch.py          scrape and clean articles from Quanta Magazine
    chunker.py        split article text into overlapping token chunks
    embed.py          generate embeddings via OpenAI API
    db.py             connect to Neon, insert chunks, search by similarity
    ingest.py         run the full ingestion pipeline over all URLs
    generate.py       build prompts and call GPT-4o-mini
    api.py            FastAPI backend exposing a /query endpoint
    app.py            Streamlit chat interface
    main.py           CLI for testing queries locally

## Corpus

- Source: Quanta Magazine (CC BY-NC-ND 4.0)
- Articles: 286
- Chunks: 2,619
- Topics: black hole physics, gravitational waves, information paradox, Hawking radiation, singularities, event horizons

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=your_key_here
DATABASE_URL=your_neon_connection_string
```

Run locally:

```bash
streamlit run app.py
```

## Disclaimer

This is a non-commercial educational portfolio project built to demonstrate RAG system design. Article content is sourced from Quanta Magazine for demonstration purposes only. All content remains the copyright of Quanta Magazine / Simons Foundation. Not intended as a substitute for scientific literature.
