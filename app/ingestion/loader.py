import os
import pandas as pd
from pypdf import PdfReader

DATA_PATH = "data/raw"


def load_documents():
    documents = []

    for file in os.listdir(DATA_PATH):
        path = os.path.join(DATA_PATH, file)

        # TXT
        if file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                documents.append(f.read())

        # PDF
        elif file.endswith(".pdf"):
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            documents.append(text)

        # CSV
        elif file.endswith(".csv"):
            df = pd.read_csv(path)
            documents.append(df.to_string())

    return documents
