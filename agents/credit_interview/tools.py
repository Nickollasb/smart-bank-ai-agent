from langchain.tools import tool
from providers import find_data, update_data

#####################################################################################################################
############# TOOLS #################################################################################################
#####################################################################################################################

@tool("calculate_new_score")
def calculate_new_score(document: str, monthly_revenue: str, employment_type: str,
                         expenses: str, dependents: str, debts: str) -> dict:
    """Calcula o novo score de crédito de um cliente pelo CPF (document)."""
    return _calculate_new_score(document, monthly_revenue, employment_type, expenses, dependents, debts)


#####################################################################################################################
############# FUNCTIONS #############################################################################################
#####################################################################################################################

def _calculate_new_score(document: str, monthly_revenue: str, employment_type: str,
                         expenses: str, dependents: str, debts: str) -> dict:
    renda_mensal = int(monthly_revenue)
    tipo_emprego = employment_type
    despesas = int(expenses)
    num_dependentes = dependents
    tem_dividas = debts
        
    peso_renda = 30
    peso_emprego = { "formal": 300, "autônomo": 200, "desempregado": 0 }
    peso_dependentes = { '0': 100, '1': 80, '2': 60, "3+": 30 }
    peso_dividas = { "sim": -100, "não": 100 }
    score = (
        (renda_mensal / (despesas + 1)) * 
        peso_renda + peso_emprego[tipo_emprego] + peso_dependentes[num_dependentes] + peso_dividas[tem_dividas]
    )

    new_score = min(max(int(score), 0), 1000)
    _update_new_score(document, new_score)
    return { "document": document, "new_score": new_score }

def _update_new_score(document: str, new_score: int) -> dict:
    """Atualiza o novo score de crédito de um cliente em 'clientes.csv' pelo CPF (document)."""
    update_data("data/clientes.csv", "cpf", document, "score", new_score)

