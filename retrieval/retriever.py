def search(query, top_k=3):
    index, texts = load_faiss_index()

    # ✅ handle empty index (cloud case)
    if index is None or len(texts) == 0:
        return []

    query_vector = model.encode([query])

    distances, indices = index.search(
        np.array(query_vector).astype("float32"),
        top_k
    )

    results = []
    for i in indices[0]:
        if i < len(texts):
            results.append({
                "text": texts[i],
                "source": f"Chunk {i}"
            })

    return results