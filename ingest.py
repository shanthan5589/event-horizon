import time
from fetch import fetch_article
from chunker import chunk_text
from embed import embed_text
from db import insert_chunk

def ingest_urls(urls_file="urls.txt"):
    # Read all URLs
    with open(urls_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"Total URLs to process: {len(urls)}")
    
    success = 0
    failed = 0

    for i, url in enumerate(urls):

        print(f"\n[{i+1}/{len(urls)}] {url}")
        
        try:
            # Fetch article
            article = fetch_article(url)
            if article is None or len(article["text"]) < 200:
                print(f"  Skipped — too short or failed to fetch")
                failed += 1
                continue

            # Chunk it
            chunks = chunk_text(article["text"], article["title"], article["url"], chunk_size=400, overlap=50)
            print(f"  {len(chunks)} chunks")

            # Embed and insert each chunk
            for chunk in chunks:
                embedding = embed_text(chunk["text"])
                insert_chunk(chunk, embedding)

            success += 1
            time.sleep(1)  # be respectful to Quanta's server

        except Exception as e:
            print(f"  Error: {e}")
            failed += 1
            continue

    print(f"\nDone. Success: {success}, Failed: {failed}")