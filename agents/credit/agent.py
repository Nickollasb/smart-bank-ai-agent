# agents/exchange_agent.py
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from agents.credit.tools import get_credit_score

def create(base_model: ChatOpenAI):
    system_prompt = (
        "Você é um agente de crédito. "
        "Você deve auxiliar o cliente na consulta de limite de crédito a partir da tool 'get_credit_score'"
        "Responda de forma objetiva e profissional, apenas dentro do contexto do assunto relativo a crédito."
    )
    return create_agent(
        model=base_model,
        tools=[get_credit_score],
        system_prompt=system_prompt
    )
