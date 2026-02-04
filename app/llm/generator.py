import requests


def generate_answer(question, chunks):
    context = "\n\n".join([c["text"] for c in chunks])


    prompt = f"""
You are a data assistant answering questions using retrieved documents.

Rules:
- Answer ONLY using provided context.
- Give a short factual answer.
- Do NOT add explanations, reasoning, proofs, examples, or extra sections.
- Do NOT include words like "Proof", "Logic", or analysis.
- Limit answer to 2–3 sentences maximum.
- If context is insufficient, say:
  "I don't have information about this in the documents."

Context:
{context}

Question:
{question}

Answer:
"""


    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",   # or llama3 if installed
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    if "response" in data:
        answer = data["response"].strip()

        # remove unwanted prefixes
        if answer.lower().startswith("answer:"):
            answer = answer.split(":", 1)[1].strip()

        return answer

    else:
        return "No answer generated."
