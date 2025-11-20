from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

def create(base_model: ChatOpenAI):
    """
    Responde o usuário de forma humana, direcionando a conversa para o contexto bancário.
    """
     
    system_prompt = (
        f"""
        Responda a mensagem do usuário de forma humana, limitando o cliente ao contexto de serviços da instituição.

        Responda APENAS a mensagem que o cliente deve receber.
        """
    )
    return create_agent(
        model=base_model,
        tools=[],
        system_prompt=system_prompt
    )
