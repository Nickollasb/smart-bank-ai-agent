import csv
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
from langchain.tools import tool


# @tool("classificar_intencao")
# def classificar_intencao(mensagem: str) -> str:
#     """Classifica a intenção do cliente."""
    
#     model = ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0,
#         api_key=os.getenv("OPENAI_API_KEY")
#     )

#     prompt = f"""
#     Você é um classificador de intenções de um assistente bancário.

#     Analise a mensagem do cliente abaixo e determine qual categoria ela representa.

#     Categorias possíveis:
#     - EXCHANGE_INTENT → qualquer pergunta sobre câmbio, cotação, valor do dólar, euro, moedas estrangeiras, taxas de conversão ou transferência internacional.
#     - CREDIT_INTENT → pedidos de crédito, empréstimo, financiamento, aumento de limite.
#     - CREDIT_INTERVIEW_INTENT → solicitações relacionadas à análise de crédito, entrevista ou avaliação de perfil.
#     - SCREENING_INTENT → quando o pedido não se enquadra claramente em nenhuma categoria.

#     Retorne apenas o identificador da categoria (por exemplo: EXCHANGE_INTENT).

#     Mensagem: "{mensagem}"
#     """

#     resp = model.invoke([{"role": "user", "content": prompt}])
#     intent = resp.content.strip().upper()

#     if intent not in {"CREDIT_INTENT", "CREDIT_INTERVIEW_INTENT", "EXCHANGE_INTENT", "SCREENING_INTENT"}:
#         intent = "SCREENING_INTENT"

#     return intent



# TODO ajustar para ler o CSV a partir de providers > read_data
@tool("autenticar_cliente")
def autenticar_cliente(cpf: str, data_nascimento: str) -> str:
    """Autentica o cliente usando clientes.csv"""
    with open("data/clientes.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        clientes = list(reader)

    for cliente in clientes:
        if cliente["cpf"] == cpf and cliente["data_nascimento"] == data_nascimento:
            return f"[AUTH_SUCESSO] {cliente['nome']}"
    
    return "[AUTH_FALHA]"
