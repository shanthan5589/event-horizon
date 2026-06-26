from collect_urls import collect_urls
from fetch import fetch_article
from chunker import chunk_text
from embed import embed_text
from retrieve import retrieve
from generate import generate
from db import search_chunks

'''
conn = get_connection()    # open connection
cur = conn.cursor()        # create cursor
cur.execute("SELECT ...")  # send query
results = cur.fetchall()   # get results
conn.commit()              # save changes (for INSERT/UPDATE)
cur.close()                # close cursor
conn.close()               # close connection
'''

# for i in urls:

#     chunks = []

#     article = fetch_article(urls)
#     chunks.extend(chunk_text(article["text"], article_title=article['title'], article_url=article['url'], chunk_size=400, overlap=50))

#     chunk_embeddings = []
#     for i in range(len(chunks)):
#         chunk_embeddings.append(embed_text(chunks[i]['text']))

def main(input_query):
    # Ask a question

    query_embedding = embed_text(input_query)

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

    answer = generate(input_query, top_chunks)

    print(answer)

    print("\n--- Sources ---")

    sources = {}
    no_dup = set()

    for i in range(len(top_chunks)):
        if top_chunks[i][2]['article_title'] not in no_dup:
            sources[i] = {'title':top_chunks[i][2]['article_title'], 'url':top_chunks[i][2]['article_url'], 'index':top_chunks[i][2]['chunk_index']}
            no_dup.add(top_chunks[i][2]['article_title'])

    for i in sources:
        print(f"Title: {sources[i]['title']}")
        print(f"URL: {sources[i]['url']}")
        print(f"Chunk Index: {sources[i]['index']}")

query = input()
main(query)