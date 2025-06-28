# FinSolve-RBAC-RAG-Chatbot 🚀

A Retrieval-Augmented Generation (RAG) chatbot with Role-Based Access Control (RBAC), built using Python, FastAPI, and Streamlit. Designed for FinTech environments to securely deliver department-specific insights on-demand.

---

## 🔧 Features

- **✅ Role-Based Access Control (RBAC)**  
  Roles: `engineering`, `finance`, `general`, `hr`, `marketing`, `c-level`  
  Each role receives access to only its permitted data.

- **🔍 Retrieval-Augmented Generation (RAG)**  
  Uses a vector store (Chroma / Qdrant / Pinecone) to index departmental documents.  
  Retrieves relevant context for each query, filtered via RBAC, and generates grounded responses using an LLM (GPT‑4 / Llama).

- **🔐 Secure Authentication**  
  FastAPI with Basic Auth (starter code provided). Replace with JWT/MFA as needed.

- **🧠 Streamlit Chat UI**  
  Interactive, secure, user-friendly interface for each role.

- **📄 Source Citations**  
  Each response includes references to original source documents for transparency and trust.

---

## 🧱 Architecture Overview

---

## ⚙️ Technologies

| Component         | Tech Stack |
|------------------|------------|
| Backend          | Python, FastAPI |
| Chat Interface   | Streamlit |
| Vector Store     | ChromaDB vectore store |
| LLM              | GPT‑4 / Llama |
| Auth             | Basic Auth (starter), can upgrade to JWT/MFA |
| Serialization    | JSON, optionally `pickle` |

---

## 🚀 Getting Started

1. **Clone the Repo**  
   ```bash
   git clone https://github.com/YOUR_USERNAME/FinSolve-RBAC-RAG-Chatbot.git
   cd FinSolve-RBAC-RAG-Chatbot


