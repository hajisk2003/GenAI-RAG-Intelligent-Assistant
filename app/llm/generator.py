
from groq import Groq
import os

# Correct: read from environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question, chunks):
    context = "\n\n".join([c["text"] for c in chunks])

    prompt = f"""
You are a helpful AI assistant.

If context is provided:
- Answer ONLY using the context
- Keep answer short (2-3 lines)

If NO context is provided:
- Answer like a normal AI assistant

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ updated model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    answer = response.choices[0].message.content.strip()

    return answer



# import requests


# def generate_answer(question, chunks):
#     context = "\n\n".join([c["text"] for c in chunks])


#     prompt = f"""
# You are a data assistant answering questions using retrieved documents.

# Rules:
# - Answer ONLY using provided context.
# - Give a short factual answer.
# - Do NOT add explanations, reasoning, proofs, examples, or extra sections.
# - Do NOT include words like "Proof", "Logic", or analysis.
# - Limit answer to 2–3 sentences maximum.
# - If context is insufficient, say:
#   "I don't have information about this in the documents."

# Context:
# {context}

# Question:
# {question}

# Answer:
# """


#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "phi",   # or llama3 if installed
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     data = response.json()

#     if "response" in data:
#         answer = data["response"].strip()

#         # remove unwanted prefixes
#         if answer.lower().startswith("answer:"):
#             answer = answer.split(":", 1)[1].strip()

#         return answer

#     else:
#         return "No answer generated."
