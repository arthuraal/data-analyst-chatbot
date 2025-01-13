from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Analytics Chatbot",
    description="Chatbot de análise de dados com FastAPI",
    version="1.0.0",
)

app.include_router(router)

@app.get("/")
def root():
    """
    Root endpoint to verify if the API is running.

    Returns:
        dict: A message confirming the API is operational.
    """
    return {"message": "API do Analytics Chatbot está funcionando!"}