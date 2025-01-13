import openai
import pandas as pd
from sqlalchemy import text, create_engine

class2desc = {
    'date': 'data de referência do registro',
    'defaulter': 'alvo binário de inadimplência (1: Mau Pagador, i.e. atraso > 60 dias em 2 meses)',
    'sex': 'sexo',
    'age': 'idade do indivíduo',
    'has_died': 'flag de óbito (indica se o indivíduo faleceu)',
    'uf': 'unidade federativa (UF) brasileira',
    'social_class': 'classe social estimada'
}


def format_table_description(table_name, columns, unique_values):
    description = f"### {table_name}\n**Descrição:**\n"
    description += f"Armazena informações relacionadas a {table_name.lower()}.\n\n"
    description += "| Nome da Coluna  | Tipo de Dados  | Restrições                          | Descrição                               | Exemplo dos valores          |\n"
    description += "|-----------------|----------------|-------------------------------------|-----------------------------------------|------------------------------|\n"
    
    for column in columns:
        col_name = column[0]
        col_type = column[1]
        col_constraints = column[2]
        col_description = class2desc.get(col_name, "Descrição não disponível")

        col_unique = ', '.join(map(str, unique_values.get(col_name, [])))
        if len(col_unique) > 50:  # Trunca valores longos
            col_unique = col_unique[:47] + ", ..."
        
        description += f"| {col_name} | {col_type} | {col_constraints} | {col_description} | {col_unique} |\n"
    
    return description


def get_structure_postgresql(connection_string):
    """Extract structure from PostgreSQL database in an optimized way.

    Args:
        connection_string: SQLAlchemy connection string for PostgreSQL.

    Returns:
        Text description of database structure (table names and their columns).
    """
    
    engine = create_engine(connection_string)

    with engine.connect() as connection:
        query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'cleaned_neurotech_data'
            ORDER BY ordinal_position;
        """

        table_structures = []
        columns_result = connection.execute(text(query))
        columns = columns_result.fetchall()


        unique_values = {}
        for column in columns:
            col_name = column[0]
            col_type = column[1]
            try:
                unique_query = f"""
                    SELECT DISTINCT {col_name}
                    FROM cleaned_neurotech_data
                    LIMIT 10; -- Limita a 10 valores para evitar overhead
                """
                unique_result = connection.execute(text(unique_query))
                unique_values[col_name] = [row[0] for row in unique_result]
            except Exception as e:
                unique_values[col_name] = ["Erro ao coletar valores únicos"]

        description = format_table_description('cleaned_neurotech_data', columns, unique_values)

    return description