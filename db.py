import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def insert_chunk(chunk, embedding):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO chunks (article_title, article_url, chunk_index, text, embedding)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            chunk["article_title"],
            chunk["article_url"],
            chunk["chunk_index"],
            chunk["text"],
            embedding
        )
    )
    conn.commit()
    cur.close()
    conn.close()

def search_chunks(query_embedding, top_k=3):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT article_title, article_url, chunk_index, text,
               1 - (embedding <=> %s::vector) AS similarity
        FROM chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (query_embedding, query_embedding, top_k)
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results