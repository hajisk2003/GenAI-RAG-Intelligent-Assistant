import os
import faiss
import pickle

VECTOR_PATH = "embeddings/vector_store"

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
# import faiss
# import numpy as np
# import pickle
# import os

# VECTOR_PATH = "embeddings/vector_store"

# def save_faiss_index(vectors, texts):
#     dim = len(vectors[0])
#     index = faiss.IndexFlatL2(dim)

#     index.add(np.array(vectors).astype("float32"))

#     os.makedirs(VECTOR_PATH, exist_ok=True)

#     faiss.write_index(index, f"{VECTOR_PATH}/index.faiss")

#     with open(f"{VECTOR_PATH}/texts.pkl", "wb") as f:
#         pickle.dump(texts, f)


# def load_faiss_index():
#     index = faiss.read_index(f"{VECTOR_PATH}/index.faiss")

#     with open(f"{VECTOR_PATH}/texts.pkl", "rb") as f:
#         texts = pickle.load(f)

#     return index, texts
