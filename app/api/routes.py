from fastapi import UploadFile, File
import shutil
import os
from app.ingestion.loader import load_documents
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import create_embeddings
from app.retrieval.vector_store import save_faiss_index

from fastapi import APIRouter
from app.retrieval.retriever import search
from app.llm.generator import generate_answer
from app.api.schema import QuestionRequest

router = APIRouter()


@router.post("/ask")
def ask_question(data: QuestionRequest):
    question = data.question

    chunks = search(question)
    answer = generate_answer(question, chunks)

    return {
    "question": question,
    "answer": answer,
    "sources": [c["source"] for c in chunks]
}
UPLOAD_DIR = "data/raw"


@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # rebuild index
    docs = load_documents()
    chunks = chunk_documents(docs)
    vectors = create_embeddings(chunks)
    save_faiss_index(vectors, chunks)

    return {"message": f"{file.filename} uploaded and indexed"}

