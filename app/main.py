from typing import Dict

from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.services.retriever import get_answer_from_docs
from pydantic import BaseModel

from app.schemas.user import QueryRequest
from app.schemas.auth import get_user_role, get_allowed_departments
from app.utils.embedder import load_or_create_vectorstore

app = FastAPI()
security = HTTPBasic()


# Dummy user database
users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"}
}


# Authentication dependency
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": username, "role": user["role"]}


# Request schema for /chat
class ChatRequest(BaseModel):
    message: str

@app.on_event("startup")
def startup_event():
    print("🚀 App is starting... Checking vector store.")
    load_or_create_vectorstore()

# --- ROUTES --- #

# Login endpoint (verifies credentials and returns role)
@app.get("/login")
def login(user=Depends(authenticate)):
    return {
        "user": user["username"],
        "role": user["role"],
        "message": f"Welcome {user['username']}!"
    }


# Test endpoint (protected route for verification)
@app.get("/test")
def test(user=Depends(authenticate)):
    return {
        "user": user["username"],
        "role": user["role"],
        "message": "You can now chat securely"
    }


# Chat endpoint (to be enhanced with document search)
@app.post("/chat")
def chat(user=Depends(authenticate), request: ChatRequest = Body(...)):
    allowed_departments = get_allowed_departments(user["role"])
    rag_result = get_answer_from_docs(request.message, allowed_departments)

    return {
        "user": user["username"],
        "role": user["role"],
        "query": request.message,
        "response": rag_result["answer"],
        "sources": rag_result["sources"]
    }


# Non-auth query test (for dev/testing - bypasses password)
@app.post("/query")
def process_query(req: QueryRequest):
    role = get_user_role(req.username)
    if not role:
        raise HTTPException(status_code=401, detail="Invalid user")

    allowed_departments = get_allowed_departments(role)

    return {
        "user": req.username,
        "role": role,
        "allowed_departments": allowed_departments,
        "query": req.query,
        "status": "Ready to fetch data in next phase"
    }
