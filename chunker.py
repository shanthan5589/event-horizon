import tiktoken

def chunk_text(text, article_title, article_url, chunk_size=400, overlap=50):
    # tiktoken tokenizer for text-embedding-3-small
    enc = tiktoken.get_encoding("cl100k_base")
    
    tokens = enc.encode(text)
    print(f"Total tokens in article: {len(tokens)}")
    
    chunks = []
    start = 0
    index = 0
    
    while start < len(tokens):

        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_str = enc.decode(chunk_tokens)

        chunks.append({
        "article_title": article_title,
        "article_url":article_url,
        "chunk_index": index,
        "text":chunk_str        })

        start += chunk_size - overlap
        index += 1
    
    return chunks