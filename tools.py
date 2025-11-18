# agents/exchange_agent.py
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from providers import http_request

# ==============================
# 🔧 TOOL: Cotação do Dólar
# ==============================

@tool("consultar_cotacao_dolar")
def consultar_cotacao_dolar() -> str:
    """Consulta a cotação atual do dólar (USD → BRL) usando a AwesomeAPI."""
    try:
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        response = http_request("GET", url)
        dollar_data = response.get("USDBRL")

        if not dollar_data:
            return "Não foi possível obter os dados do dólar no momento."

        bid_price = float(dollar_data.get("bid", 0))
        high_price = float(dollar_data.get("high", 0))
        low_price = float(dollar_data.get("low", 0))

        return (
            f"A cotação atual do dólar é **R$ {bid_price:.2f}**. "
            f"Máxima do dia: R$ {high_price:.2f}, mínima: R$ {low_price:.2f}."
        )

    except Exception as e:
        return f"Erro ao consultar cotação: {e}"


# ==============================
# 🔧 TOOL: Encerrar conversa
# ==============================

@tool("encerrar_conversa")
def encerrar_conversa() -> str:
    """Encerra o atendimento de forma educada."""
    return "Obrigado por utilizar nosso serviço. Tenha um ótimo dia!"


# ==============================
# 🧠 AGENTE DE CÂMBIO
# ==============================

def create(base_model: ChatOpenAI):
    """
    Cria o agente responsável por operações de câmbio:
    responder dúvidas sobre cotação, variação e moeda.
    """
    tools = [consultar_cotacao_dolar, encerrar_conversa]

    system_prompt = (
        "Você é um agente de câmbio financeiro. "
        "Responda perguntas sobre cotação, dólar, euro e conversões. "
        "Se o usuário pedir o valor do dólar, use a ferramenta 'consultar_cotacao_dolar'. "
        "Responda de forma objetiva e profissional."
    )

    return create_agent(
        model=base_model,
        tools=tools,
        system_prompt=system_prompt
    )
