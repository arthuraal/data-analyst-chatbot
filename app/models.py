from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    model: str

class State(BaseModel):
    question: str
    query: str
    result: str
    answer: str