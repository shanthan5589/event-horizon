from embed import embed_text, cosine_similarity

# Embed all chunks
def retrieve(chunks, embeddings, input_query, top_k=3):

    # Global Chunk index, Local Chunk index

    # Now search
    query_embedding = embed_text(input_query)

    # Score every chunk
    scores = []
    for i, emb in enumerate(embeddings):
        score = cosine_similarity(query_embedding, emb)
        scores.append((score, i, chunks[i])) 
        # Above Line:
            # chunks[i] is a dictionary consisting of Local Chunk Index 
            # (score, i, chunks[i]) in this "i" is the Global Chunk Index
            # The order of embeddings and chunks are same as we are using a list.
         

    # Sort by score descending
    scores.sort(reverse=True)

    return scores[:top_k]