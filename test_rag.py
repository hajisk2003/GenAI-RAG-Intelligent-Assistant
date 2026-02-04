from app.retrieval.retriever import search
from app.llm.generator import generate_answer

question = "What causes road accidents ?"

chunks = search(question)

answer = generate_answer(question, chunks)

print("\nAnswer:\n")
print(answer)
