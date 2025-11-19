from langchain.tools import tool
from providers import http_request


@tool("check_currency_exchange_rate")
def check_currency_exchange_rate(currency: str = "USD") -> str:
    """
    Consulta a cotação de QUALQUER moeda para BRL usando a AwesomeAPI.

    Exemplos de uso:
    - consultar_cotacao("USD")
    - consultar_cotacao("EUR")
    - consultar_cotacao("GBP")
    - consultar_cotacao("BTC")
    """
    
    try:
        currency = currency.upper().strip()

        if not currency.isalpha() or len(currency) > 5:
            return f"Moeda inválida: {currency}. Tente algo como USD, EUR, GBP, BTC."

        url = f"https://economia.awesomeapi.com.br/json/last/{currency}-BRL"

        response = http_request("GET", url)
        pair_key = f"{currency}BRL"
        data = response.get(pair_key)

        if not data:
            return f"Não encontrei cotação para {currency} → BRL no momento."

        bid = float(data.get("bid", 0))

        return (
            f"A cotação atual de {currency} → BRL é R$ {bid:.2f}."
        )

    except Exception as e:
        return f"Erro ao consultar cotação de {currency}: {e}"
