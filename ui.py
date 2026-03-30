import streamlit as st
import os

# RAG imports
from app.llm.generator import generate_answer
from app.ingestion.loader import load_documents
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import create_embeddings
from app.retrieval.vector_store import save_faiss_index
from app.retrieval.retriever import search

st.set_page_config(page_title="GenAI RAG Assistant", layout="wide")

st.title("🤖 GenAI RAG Assistant")

# ---------- Sidebar ----------
st.sidebar.header("📂 Document Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF / CSV / TXT",
    type=["pdf", "csv", "txt"]
)

# ---------- Upload Handling ----------
if uploaded_file:
    os.makedirs("data/raw", exist_ok=True)
    file_path = os.path.join("data/raw", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Run ingestion pipeline
    docs = load_documents()
    chunks = chunk_documents(docs)
    vectors = create_embeddings(chunks)
    save_faiss_index(vectors, chunks)

    st.sidebar.success("✅ File uploaded & indexed!")

# ---------- Clear Chat ----------
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------- Chat Memory ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------- User Input ----------
question = st.chat_input("Ask questions from your documents...")

if question:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    st.chat_message("user").write(question)

    with st.spinner("Thinking..."):
        chunks = search(question)

        # ✅ If NO document data → use general AI
        if not chunks:
            answer = generate_answer(question, [])
            sources = []
        else:
            answer = generate_answer(question, chunks)
            sources = [f"Document section {i+1}" for i in range(len(chunks))]

    # Format answer
    answer_text = answer

    if sources:
        answer_text += "\n\n📚 Sources:\n"
        for s in sources:
            answer_text += f"- {s}\n"

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": answer_text}
    )

    st.chat_message("assistant").write(answer_text)
# import streamlit as st
# import requests
# API_URL = "http://127.0.0.1:8000/ask"
# UPLOAD_URL = "http://127.0.0.1:8000/upload"

# st.set_page_config(page_title="GenAI RAG Assistant", layout="wide")

# st.title("🤖 GenAI RAG Assistant")

# # ---------- Sidebar ----------
# st.sidebar.header("📂 Document Upload")

# uploaded_file = st.sidebar.file_uploader(
#     "Upload PDF or CSV",
#     type=["pdf", "csv", "txt"]
# )

# if uploaded_file:
#     files = {"file": uploaded_file.getvalue()}
#     response = requests.post(
#         UPLOAD_URL,
#         files={"file": (uploaded_file.name, uploaded_file)}
#     )
#     st.sidebar.success("File uploaded & indexed!")

# if st.sidebar.button("🧹 Clear Chat"):
#     st.session_state.messages = []
#     st.rerun()

# # ---------- Chat Memory ----------
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # show chat history
# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# # ---------- User Input ----------
# question = st.chat_input("Ask questions from your documents...")

# if question:
#     st.session_state.messages.append(
#         {"role": "user", "content": question}
#     )
#     st.chat_message("user").write(question)

#     with st.spinner("Thinking..."):
#         response = requests.post(API_URL, json={"question": question})
#         data = response.json()

#     answer = data["answer"]
#     sources = data.get("sources", [])

#     answer_text = answer

#     if sources:
#         answer_text += "\n\n📚 Sources:\n"
#         for s in sources:
#             answer_text += f"- {s}\n"

#     st.session_state.messages.append(
#         {"role": "assistant", "content": answer_text}
#     )

#     st.chat_message("assistant").write(answer_text)
