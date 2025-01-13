from fastapi import APIRouter, HTTPException
from app.services import process_question
from app.models import QueryRequest
from datetime import datetime

router = APIRouter()

@router.post("/query/")
def query_data(request: QueryRequest):
    """
    Endpoint to process user questions.

    This endpoint receives a user's question and model choice as input, processes
    the question using the specified model, and returns the results.

    Args:
        request (QueryRequest): A Pydantic model containing:
            - `question` (str): The user's natural language question.
            - `model` (str): The model selected to process the question (e.g., OpenAI or Bedrock).
            
    Returns:
        dict: A dictionary containing the result of the processed query.

    Raises:
        HTTPException: If an error occurs during question processing, an HTTP 500 error 
        is returned with the error details.
    """
    try:
        start_time = datetime.now()
        result = process_question(request.question, request.model)
        execution_time = (datetime.now() - start_time).total_seconds()
        return {"result": result, "model": request.model, "execution_time": execution_time}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))