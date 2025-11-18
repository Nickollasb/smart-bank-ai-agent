from langchain.tools import tool
from providers import read_data
import csv
from datetime import datetime

@tool("get_credit_score")
def get_credit_score(document: str) -> dict:
    """Consulta o score de crédito de um cliente pelo CPF (document)."""

    for row in read_data("data/clientes.csv"):
        if row.get('cpf') == document:
            return f"{row['score']}"
        
    return "CUSTOMER_SCORE_NOT_FOUND"

@tool("get_current_credit_limit")
def get_current_credit_limit(document: str) -> dict:
    """Consulta o limite de crédito de um cliente pelo CPF (document)."""

    for row in read_data("data/clientes.csv"):
        if row.get('cpf') == document:
            return f"{row['limite_credito']}"
        
    return "CUSTOMER_SCORE_NOT_FOUND"


### TODO REVISAR daqui pra baixo

@tool("check_score_for_new_limit")
def check_score_for_new_limit(document: str, new_limit: float) -> str:
    """
    Verifica se o score do cliente permite o novo limite desejado.
    Retornos possíveis:
        - APROVADO
        - REPROVADO
    """

    score = get_credit_score(document)

    # TODO ajustar para direcionar para a entrevista de crédito
    if score is None:
        return "REPROVADO"

    with open("data/score_limite.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            faixa_min = float(row["score_min"])
            faixa_max = float(row["score_max"])
            limite_max = float(row["limite_max"])

            if faixa_min <= score <= faixa_max:
                return "APROVADO" if new_limit <= limite_max else "REPROVADO"

    return "REPROVADO"


@tool("register_request_for_limit_increase")
def register_request_for_limit_increase(
    document: str,
    current_limit: float,
    new_limit: float,
    status: str
) -> str:
    """
    Registra o pedido de aumento de limite no CSV solicitacoes_aumento_limite.csv
    """
    file_path = "data/solicitacoes_aumento_limite.csv"

    header = [
        "cpf_cliente",
        "data_hora_solicitacao",
        "limite_atual",
        "novo_limite_solicitado",
        "status_pedido"
    ]

    now = datetime.now().isoformat()

    row = {
        "cpf_cliente": document,
        "data_hora_solicitacao": now,
        "limite_atual": current_limit,
        "novo_limite_solicitado": new_limit,
        "status_pedido": status
    }

    # Garante que o arquivo exista com header
    try:
        with open(file_path, "x", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
    except FileExistsError:
        pass

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writerow(row)

    return "OK"