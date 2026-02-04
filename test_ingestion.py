from app.ingestion.loader import load_documents
from app.ingestion.chunker import chunk_documents

docs = load_documents()
chunks = chunk_documents(docs)

print("Loaded docs:", len(docs))
print("Total chunks:", len(chunks))
print("\nFirst chunk:\n", chunks[0])
