from langchain_openai import ChatOpenAI
from providers import create_agent_provider
from agents.exchange.tools import check_currency_exchange_rate

def create(base_model: ChatOpenAI):
    system_prompt = (
        "Você é um agente de câmbio. "
        "Forneça informações sobre cotações de moedas, conversões e variações cambiais."
    )
    
    return create_agent_provider(base_model, system_prompt, tools=[check_currency_exchange_rate],)
