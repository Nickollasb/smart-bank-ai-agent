from langchain.tools import tool
from providers import read_data, update_data

# @tool("calculate_new_score")
def calculate_new_score(document: str) -> dict:
    """Calcula o novo score de crédito de um cliente pelo CPF (document)."""
    customer = None
    renda_mensal = 5000
    tipo_emprego = "formal"
    despesas = 12000
    num_dependentes = 1
    tem_dividas = "não"
    
    for row in read_data("data/clientes.csv"):
        if row.get('cpf') == document:
            customer = row
            break 
        
    peso_renda = 30
    peso_emprego = {
        "formal": 300,
        "autônomo": 200,
        "desempregado": 0
    }
    peso_dependentes = {
        0: 100,
        1: 80,
        2: 60,
        "3+": 30
    }
    peso_dividas = {
        "sim": -100,
        "não": 100
    }

    score = (
        (renda_mensal / (despesas + 1)) * 
        peso_renda + peso_emprego[tipo_emprego] + peso_dependentes[num_dependentes] + peso_dividas[tem_dividas]
    )

    return {"cpf": document, "new_score": min(max(int(score), 0), 1000)}

# @tool("update_new_score")
def update_new_score(document: str, new_score: int) -> dict:
    """Atualiza o novo score de crédito de um cliente em 'clientes.csv' pelo CPF (document)."""
    
    column_name = 'cpf'    
    update_data("data/clientes.csv", column_name, document, new_score)

    return "Sucesso na atualização do score de crédito."

