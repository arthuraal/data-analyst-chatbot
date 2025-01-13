def prompt_sql_to_text(state: dict) -> str:
    """
    Generate a natural language answer based on the SQL query result.

    This function takes the user's question, the SQL query, and the query result, 
    and generates a natural language answer by formatting them into a structured prompt.

    Args:
        state (dict): A dictionary containing the following keys:
            - "question" (str): The user's natural language question.
            - "query" (str): The SQL query corresponding to the user's question.
            - "result" (str): The result of the executed SQL query.

    Returns:
        str: A formatted prompt to generate a natural language answer.
    """
    prompt = (
        "Dada a seguinte pergunta do usuário, consulta SQL correspondente,"
        "e resultado SQL, responda a pergunta do usuário.\n\n"
        f'Pergunta: {state["question"]}\n'
        f'Consulta SQL: {state["query"]}\n'
        f'Resultado SQL: {state["result"]}'
    )
    return prompt


def prompt_text_to_sql(table_info: str, question: str) -> str:
    """
    Generate a prompt to translate a natural language question into a SQL query.

    This function generates a structured prompt to instruct a language model 
    to translate a user question into a syntactically correct SQL query. It ensures 
    the query adheres to the database structure and constraints.

    Args:
        table_info (str): A description of the database schema, listing the tables 
                          and their respective columns.
        question (str): The user's question in natural language.

    Returns:
        str: A formatted prompt for translating the question into a SQL query.
    """

    prompt = f"""
    # Contexto
    Você é um especialista em PostgreSQL. Seu trabalho é ajudar os usuários com suas perguntas de negócios, analisando os dados contidos em um banco de dados PostgreSQL.

    # Instruções:
    1. Dada uma pergunta de entrada, primeiro crie uma consulta PostgreSQL sintaticamente correta para executar, depois observe os resultados da consulta e forneça a resposta à pergunta de entrada.
    2. A menos que o usuário especifique na pergunta um número específico de exemplos a serem obtidos, consulte no máximo 5 resultados usando a cláusula LIMIT conforme o padrão do PostgreSQL. Você pode ordenar os resultados para retornar os dados mais informativos no banco de dados.
    3. Nunca consulte todas as colunas de uma tabela. Você deve consultar apenas as colunas necessárias para responder à pergunta. Envolva cada nome de coluna com aspas duplas (") para marcá-las como identificadores delimitados.
    4. Certifique-se de usar apenas os nomes das colunas visíveis nas tabelas abaixo. Tenha cuidado para não consultar colunas que não existem. Além disso, preste atenção a qual coluna está em qual tabela.
    5. Responda apenas perguntas que tenham relação com o CONTEXTO FORNECIDO.

    Use apenas as seguintes tabelas:
    {table_info}

    Pergunta em linguagem natural:
    {question}
    """
    return prompt