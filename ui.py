import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"
UPLOAD_URL = "http://127.0.0.1:8000/upload"

st.set_page_config(page_title="GenAI RAG Assistant", layout="wide")

st.title("🤖 GenAI RAG Assistant")

# ---------- Sidebar ----------
st.sidebar.header("📂 Document Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF or CSV",
    type=["pdf", "csv", "txt"]
)

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(
        UPLOAD_URL,
        files={"file": (uploaded_file.name, uploaded_file)}
    )
    st.sidebar.success("File uploaded & indexed!")

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
        response = requests.post(API_URL, json={"question": question})
        data = response.json()

    answer = data["answer"]
    sources = data.get("sources", [])

    answer_text = answer

    if sources:
        answer_text += "\n\n📚 Sources:\n"
        for s in sources:
            answer_text += f"- {s}\n"

    st.session_state.messages.append(
        {"role": "assistant", "content": answer_text}
    )

    st.chat_message("assistant").write(answer_text)
