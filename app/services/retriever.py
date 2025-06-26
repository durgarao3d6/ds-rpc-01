from langchain_openai import OpenAIEmbeddings
from langchain_chroma.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

CHROMA_DB_PATH = "vector_store"

def get_answer_from_docs(query: str, allowed_departments: list[str]):
    embeddings = OpenAIEmbeddings()  # latest import :contentReference[oaicite:1]{index=1}
    db = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )  # updated vector store import :contentReference[oaicite:2]{index=2}

    retriever = db.as_retriever(search_kwargs={
        "k": 3,
        "filter": {"department": {"$in": allowed_departments}}
    })

    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        retriever=retriever,
        return_source_documents=True
    )

    result = qa_chain({"query": query})
    return {
        "answer": result["result"],
        "sources": [doc.metadata for doc in result["source_documents"]]
    }
