import os
from pathlib import Path
import sys
from typing import List
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from typing import List
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

CHROMA_DB_PATH = "vector_store"

def load_documents(data_dir: str = "resources/data") -> List[Document]:
    docs = []
    for dept_folder in Path(data_dir).iterdir():
        if dept_folder.is_dir():
            for file in dept_folder.glob("*.*"):
                if file.suffix == ".md":
                    loader = TextLoader(str(file), encoding='utf-8')
                elif file.suffix == ".csv":
                    loader = CSVLoader(str(file), encoding='utf-8')
                else:
                    print(f"⚠️ Skipping unsupported file: {file}")
                    continue

                pages = loader.load()
                for page in pages:
                    page.metadata["department"] = dept_folder.name
                    page.metadata["source"] = file.name
                docs.extend(pages)
    return docs

def embed_and_store_documents(documents: List[Document]):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=CHROMA_DB_PATH)
    db.persist()
    print(f"✅ Embedded {len(chunks)} chunks and stored them in ChromaDB.")

def load_or_create_vectorstore():
    if not Path(CHROMA_DB_PATH).exists():
        print("📦 No vector DB found. Creating new one...")
        docs = load_documents()
        embed_and_store_documents(docs)
    else:
        print("✅ Vector store already exists.")
