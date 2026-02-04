from sentence_transformers import SentenceTransformer


def get_embedding_model():
    # small, fast, high quality model
    return SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    model = get_embedding_model()
    vectors = model.encode(chunks)

    return vectors
