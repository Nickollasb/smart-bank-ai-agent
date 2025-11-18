from langchain.tools import tool

@tool("consultar_cotacao")
def consultar_cotacao(moeda: str = "USD", base: str = "BRL") -> str:
    """Retorna a cotação aproximada entre duas moedas (ex: USD -> BRL)."""
    # Simulação simplificada
    if moeda.upper() == "USD" and base.upper() == "BRL":
        return "O valor atual do dólar em BRL é aproximadamente R$ 5,60."
    else:
        return f"A cotação de {moeda.upper()} para {base.upper()} não está disponível no momento."