from dotenv import load_dotenv
import os
import re
from openai import OpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from app.query_execution import execute_query
from app.model_handler import ModelHandler, OpenAIStrategy, BedrockStrategy
from app.prompts import prompt_text_to_sql, prompt_sql_to_text


def process_question(question: str, model: str) -> dict:
    """
    Process a user question and return results.

    This function processes a natural language question by:
    1. Translating it into a SQL query using the selected language model (LLM).
    2. Executing the generated SQL query against a PostgreSQL database.
    3. Generating a natural language answer based on the SQL query result.

    Args:
        question (str): The user's question in natural language.
        model (str): The language model to use for processing (e.g., "GPT-4o mini" or "Llama 3.3 70B Instruct").

    Returns:
        dict: A dictionary containing the generated response message or an error message.

    Raises:
        ValueError: If the specified model is not supported.
    """

    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_ENDPOINT = os.getenv("DB_ENDPOINT")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ENDPOINT}:{DB_PORT}/{DB_NAME}"

    db = SQLDatabase.from_uri(connection_string)
    table_info = db.get_table_info()

    try:
        prompt = prompt_text_to_sql(table_info, question)

        if model == "GPT-4o mini":
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            strategy = OpenAIStrategy(api_key=OPENAI_API_KEY)
        elif model == "Llama 3.3 70B Instruct":
            AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
            AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
            strategy = BedrockStrategy(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
        else:
            raise ValueError(f"Model {model} not supported.")

        handler = ModelHandler(strategy=strategy)
        response = handler.generate_response(prompt)

        query_match = re.search(r"```sql(.*?)```", response, re.DOTALL)
        if not query_match:
            return {"message": "Unable to generate a valid SQL query."}
        
        query = query_match.group(1).strip()

        query_result = execute_query(query, db)

        prompt = prompt_sql_to_text({"query": query, "result": query_result, "question": question})
        answer = handler.generate_response(prompt)

        return {"message": answer}

    except Exception as error:
        return {"message": "Unable to generate a valid SQL query."}
