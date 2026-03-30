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
    index_path = f"{VECTOR_PATH}/index.faiss"
    text_path = f"{VECTOR_PATH}/texts.pkl"

    if not os.path.exists(index_path) or not os.path.exists(text_path):
        return None, []

    index = faiss.read_index(index_path)

    with open(text_path, "rb") as f:
        texts = pickle.load(f)

    return index, texts
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
