import streamlit as st
import os

# import your RAG functions
# from app.retrieval.search import search
from app.llm.generator import generate_answer
from app.ingestion.loader import load_documents
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import create_embeddings
from app.retrieval.vector_store import save_faiss_index
st.set_page_config(page_title="GenAI RAG Assistant", layout="wide")

st.title("🤖 GenAI RAG Assistant")

# ---------- Sidebar ----------
st.sidebar.header("📂 Document Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF / CSV / TXT",
    type=["pdf", "csv", "txt"]
)

# handle upload
if uploaded_file:
    # save file locally
    os.makedirs("data/raw", exist_ok=True)
    file_path = os.path.join("data/raw", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # re-run ingestion pipeline
    docs = load_documents()
    chunks = chunk_documents
    vectors = create_embeddings(chunks)
    save_faiss_index(vectors, chunks)
    st.sidebar.success("File uploaded & indexed!")

# clear chat
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------- Chat Memory ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# show chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------- User Input ----------
question = st.chat_input("Ask questions from your documents...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    st.chat_message("user").write(question)

    with st.spinner("Thinking..."):
        # 🔥 DIRECT RAG CALL (NO API)
        chunks = search(question)
        answer = generate_answer(question, chunks)

    # sources
    sources = [c.get("source", "chunk") for c in chunks]

    answer_text = answer

    if sources:
        answer_text += "\n\n📚 Sources:\n"
        for s in sources:
            answer_text += f"- {s}\n"

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
