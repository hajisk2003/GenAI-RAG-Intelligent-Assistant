from app.ingestion.loader import load_documents
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import create_embeddings
from app.retrieval.vector_store import save_faiss_index

docs = load_documents()
chunks = chunk_documents(docs)

print("Creating embeddings...")
vectors = create_embeddings(chunks)

print("Saving vector DB...")
save_faiss_index(vectors, chunks)

print("Done!")
