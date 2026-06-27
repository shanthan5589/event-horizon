---
title: Event Horizon
sdk: docker
pinned: false
---

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

    get_page_urls.py  extract article links from a single search results page
    collect_urls.py   collect all article URLs across paginated search results
    fetch.py          scrape and clean article text from a URL
    chunker.py        split article text into overlapping token chunks
    embed.py          generate embeddings via OpenAI API
    db.py             store chunks and embeddings in PostgreSQL, search by similarity
    ingest.py         run the full pipeline: fetch, chunk, embed, store
    generate.py       build prompts and call GPT-4o-mini with retrieved context
    api.py            FastAPI backend exposing a /query endpoint
    app.py            Streamlit chat interface


## Corpus

- Source: Quanta Magazine (all rights reserved — © Simons Foundation)
- Articles: 286 (scraped for educational/portfolio demonstration purposes only)
- Chunks: 2,619
- Topics: black hole physics, gravitational waves, information paradox, Hawking radiation, singularities, event horizons, and related areas

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

This is a **non-commercial educational portfolio project** created to demonstrate Retrieval-Augmented Generation (RAG) techniques.

It is **not affiliated with, endorsed by, or sponsored by** Quanta Magazine or the Simons Foundation.

All article content was obtained via scraping solely for personal learning and portfolio showcase purposes. The full articles remain the copyright of Quanta Magazine / Simons Foundation. This project uses limited excerpts/chunks with proper citations back to the originals. No commercial use is made of the material. It is not intended as a substitute for reading the original articles on quantamagazine.org or for scientific literature.

Users are strongly encouraged to visit the source articles directly.

## Ethical Note

This project was built as a technical demonstration of RAG systems. In a production environment or for any public/commercial use, I would rely exclusively on openly licensed datasets (e.g., arXiv papers with permissive licenses) and seek explicit permission before using copyrighted material at scale.

The project respects `robots.txt` where feasible and was rate-limited during data collection.

## License

The **code** (Python scripts, FastAPI backend, Streamlit UI, etc.) in this repository is open source and licensed under the MIT License.

However, the **scraped article content**, text chunks, and embeddings from Quanta Magazine are **not** included under this license. They remain the copyright of Quanta Magazine / Simons Foundation and are used here only for educational/portfolio purposes.

Redistributing the raw Quanta content or derived data is not permitted.