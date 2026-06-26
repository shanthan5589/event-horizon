from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import search_chunks
from embed import embed_text
from generate import generate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query(request: QueryRequest):
    # Embed question
    query_embedding = embed_text(request.question)
    
    # Retrieve chunks
    results = search_chunks(query_embedding, top_k=3)
    
    top_chunks = []
    for row in results:
        chunk = {
            "article_title": row[0],
            "article_url": row[1],
            "chunk_index": row[2],
            "text": row[3],
            "similarity": row[4]
        }
        top_chunks.append((row[4], row[2], chunk))
    
    # Generate answer
    answer = generate(request.question, top_chunks)
    
    # Build sources
    sources = {}
    no_dup = set()

    for i in range(len(top_chunks)):
        if top_chunks[i][2]['article_title'] not in no_dup:
            sources[i] = {'title':top_chunks[i][2]['article_title'], 'url':top_chunks[i][2]['article_url'], 'index':top_chunks[i][2]['chunk_index']}
            no_dup.add(top_chunks[i][2]['article_title'])

    return {
        'answer':answer, 
        'sources':sources
    }

@app.get("/health")
def health():
    return {"status": "ok"}