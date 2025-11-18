# agents/exchange_agent.py
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from agents.exchange.tools import consultar_cotacao

def create(base_model: ChatOpenAI):
    system_prompt = (
        "Você é um agente de câmbio. "
        "Forneça informações sobre cotações de moedas, conversões e variações cambiais."
    )
    return create_agent(
        model=base_model,
        tools=[consultar_cotacao],
        system_prompt=system_prompt
    )
