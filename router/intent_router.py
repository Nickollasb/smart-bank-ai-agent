from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

def create(base_model: ChatOpenAI):
    """
    Classifica a intenção do usuário a partir do input informado
    """
     
    system_prompt = (
        f"""
        Classifique a intenção do cliente em apenas UMA das opções:
        
        - SMALL_TALK (cumprimentos, conversa fiada, assuntos gerais, despedida e.g "obrigado", "valeu", "tchau", "encerrar")
        - CREDIT_INTENT (limite, solicitar novo limite de crédito, score de crédito)
        - CREDIT_INTERVIEW_INTENT (realiza entrevista com o cliente coletando dados para saber se é possível aumentar seu limite de crédito)
        - EXCHANGE_INTENT (câmbio, dólar, euro, moedas, cotação)

        Informações adicionais:
        - Responda com apenas uma opção.
        """
    )
    return create_agent(
        model=base_model,
        tools=[],
        system_prompt=system_prompt
    )
