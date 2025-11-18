from langchain.tools import tool
from providers import read_data

@tool("get_credit_score")
def get_credit_score(document: str = "05613638110") -> dict:
    """Consulta o score de crédito de um cliente pelo CPF (document)."""
    customer = None
    for row in read_data("data/clientes.csv"):
        if row.get('cpf') == document:
            customer = row
            break 

    return customer