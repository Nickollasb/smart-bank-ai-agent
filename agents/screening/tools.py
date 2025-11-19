from langchain.tools import tool
from providers import find_data

#####################################################################################################################
############# TOOLS #################################################################################################
#####################################################################################################################

@tool("authenticate_customer")
def authenticate_customer(document: str, birth_date: str) -> str:
    """Autentica o cliente usando a tabela 'clientes.csv'"""

    return _authenticate_customer(document, birth_date)


#####################################################################################################################
############# FUNCTIONS #############################################################################################
#####################################################################################################################

def _authenticate_customer(document: str, birth_date: str) -> str:
    customers: list[dict] = find_data("data/clientes.csv", "cpf", document)

    for customer in customers:
        if customer["cpf"] == document and customer["data_nascimento"] == birth_date:
            return f"[AUTH_SUCCESS] {customer['nome']}"

    return "[AUTH_FAILED]"
