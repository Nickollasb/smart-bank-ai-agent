from providers import http_request

# TODO: Refactor to use a more generic approach for currency quotations
def get_dollar_quotation() -> str:
    """Fetches the latest USD to BRL exchange rate."""
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    
    response = http_request("GET", url)
    dollar_data = response.get("USDBRL")
    
    if dollar_data:
        bid_price = float(dollar_data.get("bid"))
        return f"BRL {bid_price:.2f}"
    else:
        print("Could not find USD/BRL data in the response.")
        return None
    
def finish_conversation() -> str:
    """Returns a message indicating the end of the conversation."""
    return "Thank you for using our service. Have a great day!"