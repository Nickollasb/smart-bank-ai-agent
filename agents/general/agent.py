from langchain_openai import ChatOpenAI
from providers import create_agent_provider

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

    return create_agent_provider(base_model, system_prompt)
