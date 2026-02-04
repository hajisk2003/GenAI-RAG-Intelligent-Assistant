import faiss
import numpy as np
import pickle
import os

VECTOR_PATH = "embeddings/vector_store"

def save_faiss_index(vectors, texts):
    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)

    index.add(np.array(vectors).astype("float32"))

    os.makedirs(VECTOR_PATH, exist_ok=True)

    faiss.write_index(index, f"{VECTOR_PATH}/index.faiss")

    with open(f"{VECTOR_PATH}/texts.pkl", "wb") as f:
        pickle.dump(texts, f)


def load_faiss_index():
    index = faiss.read_index(f"{VECTOR_PATH}/index.faiss")

    with open(f"{VECTOR_PATH}/texts.pkl", "rb") as f:
        texts = pickle.load(f)

    return index, texts
