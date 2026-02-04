from app.retrieval.retriever import search

query = "What causes road accidents?"

results = search(query)

print("\nTop relevant chunks:\n")

for i, chunk in enumerate(results):
    print(f"\nResult {i+1}:\n{chunk}")
