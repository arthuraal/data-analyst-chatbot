from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_core.language_models.llms import LLM
from sqlalchemy.engine import Engine


def execute_query(query, db: Engine):
    """
    Execute SQL query using the QuerySQLDatabaseTool.
    
    Args:
        state (dict): Estado contendo a consulta SQL.
        db (Engine): Instância do banco de dados.

    Returns:
        dict: Resultado da consulta SQL.
    """
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    result = execute_query_tool.invoke(query)
    return result


