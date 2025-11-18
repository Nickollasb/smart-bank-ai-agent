from langchain.tools import tool
from providers import http_request

@tool("consultar_cotacao")
def consultar_cotacao(moeda: str = "USD") -> str:
    """
    Consulta a cotação de QUALQUER moeda para BRL usando a AwesomeAPI.
    
    Exemplos de uso:
    - consultar_cotacao("USD")
    - consultar_cotacao("EUR")
    - consultar_cotacao("GBP")
    - consultar_cotacao("BTC")
    """

    try:
        moeda = moeda.upper().strip()

        if not moeda.isalpha() or len(moeda) > 5:
            return f"Moeda inválida: {moeda}. Tente algo como USD, EUR, GBP, BTC."

        url = f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL"

        response = http_request("GET", url)
        pair_key = f"{moeda}BRL"
        data = response.get(pair_key)

        if not data:
            return f"Não encontrei cotação para {moeda} → BRL no momento."

        bid = float(data.get("bid", 0))

        return (
            f"A cotação atual de {moeda} → BRL é R$ {bid:.2f}."
        )

    except Exception as e:
        return f"Erro ao consultar cotação de {moeda}: {e}"