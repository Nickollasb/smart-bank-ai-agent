from langchain.tools import tool
from providers import read_data, insert_data, get_current_datetime, update_data
import csv
from datetime import datetime

#####################################################################################################################
############# TOOLS #################################################################################################
#####################################################################################################################

@tool("get_credit_score")
def get_credit_score(document: str) -> dict:
    """Consulta na tabela 'clientes.csv' o score de crédito de um cliente pelo CPF (document)."""
    return _get_credit_score(document)


@tool("get_current_credit_limit")
def get_current_credit_limit(document: str) -> dict:
    """Consulta na tabela 'clientes.csv' o limite de crédito de um cliente pelo CPF (document)."""
    return _get_current_credit_limit(document)


@tool("check_score_for_new_limit")
def check_score_for_new_limit(document: str, new_limit: float) -> str:
    """
    Verifica se o score do cliente permite o novo limite desejado.
    Retornos possíveis:
        - APROVADO
        - REPROVADO
    """
    return _check_score_for_new_limit(document, new_limit)


#####################################################################################################################
############# FUNCTIONS #############################################################################################
#####################################################################################################################

def _get_credit_score(document: str) -> dict:
    for row in read_data("data/clientes.csv"):
        if row.get('cpf') == document:
            score = row['score']
            
            if not score:
                score = 0
                update_data("data/clientes.csv", "cpf", document, "score", score)

            return f"{score}"

    return "CUSTOMER_SCORE_NOT_FOUND"


def _get_current_credit_limit(document: str) -> dict:
    for row in read_data("data/clientes.csv"):
        if row.get('cpf') == document:
            limit = row['limite_credito']

            if not limit:
                limit = 0
                update_data("data/clientes.csv", "cpf", document, "limite_credito", limit)
                

            return f"{limit}"

    return "CUSTOMER_LIMIT_NOT_FOUND"


def _check_score_for_new_limit(document: str, new_limit: float) -> str:
    new_limit_request_status = "REPROVADO"
    score = _get_credit_score(document)

    if score is None:
        _register_request_for_limit_increase(document, new_limit, new_limit_request_status)
        return new_limit_request_status

    with open("data/score_limite.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            faixa_min = float(row["score_min"])
            faixa_max = float(row["score_max"])
            limite_max = float(row["limite_max"])

            if (faixa_min <= int(score) <= faixa_max) and (new_limit <= limite_max):
                new_limit_request_status = "APROVADO"
                _register_request_for_limit_increase(document, new_limit, new_limit_request_status)
                _update_increase_new_customer_limit(document, new_limit)
                return new_limit_request_status

    _register_request_for_limit_increase(document, new_limit, new_limit_request_status)
    return new_limit_request_status


def _register_request_for_limit_increase(document, new_limit, new_limit_request_status):
    insert_data("data/solicitacoes_aumento_limite.csv", {
        "cpf_cliente": document,
        "data_hora_solicitacao": get_current_datetime(),
        "limite_atual": _get_current_credit_limit(document),
        "novo_limite_solicitado": new_limit,
        "status_pedido": new_limit_request_status
    })

def _update_increase_new_customer_limit(document, new_limit):
    update_data('data/clientes.csv', "cpf", document, "limite_credito", new_limit)