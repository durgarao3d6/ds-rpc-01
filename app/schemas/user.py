from pydantic import BaseModel

class User(BaseModel):
    username: str
    role: str

class QueryRequest(BaseModel):
    username: str
    query: str
