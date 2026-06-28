from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import search_chunks
from embed import embed_text
from generate import generate

from openai import OpenAI

app = FastAPI()
client = OpenAI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

history = []

@app.post("/query")
def query(request: QueryRequest):
    # Embed question
    if not history:
        rephrased_question = request.question
    else:
        prompt = f"""You are rewriting a user's question so it can stand on its own for a search system.
                    Using the conversation history, rewrite the user's latest question into a single, 
                    self-contained question. Resolve any pronouns or references like "it", "that", "this thing" 
                    into the specific subject from the history (e.g. the specific black hole being discussed).
                    Return ONLY the rewritten question. No preamble, no explanation, no quotation marks.
                    Context: {history} 
                    Question: {request.question}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
            )
        
        rephrased_question = response.choices[0].message.content.strip()
        
    query_embedding = embed_text(rephrased_question)

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
    answer = generate(rephrased_question, top_chunks)

    history.append({'role':"user",  "content":request.question})
    history.append({ 'role':"assistant", 'content':answer})

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