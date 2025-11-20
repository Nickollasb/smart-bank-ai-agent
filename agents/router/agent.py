from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

def create(base_model: ChatOpenAI):
    """
    Classifica a intenção do usuário a partir do input informado
    """
     
    system_prompt = (
        f"""
        Com base no contexto, classifique a intenção do cliente em apenas UMA das opções abaixo:
        - SMALL_TALK (ex: cumprimentos, conversa fiada, assuntos gerais, despedida e.g "obrigado", "valeu", "tchau", "encerrar")
        - CREDIT_INTENT (ex: limite, solicitar novo limite de crédito, score de crédito)
        - CREDIT_INTERVIEW_INTENT (ex: realiza entrevista com o cliente coletando dados para saber se é possível aumentar seu limite de crédito)
        - EXCHANGE_INTENT (ex: câmbio, dólar, euro, moedas, cotação)

        Informações adicionais:
        - Responda com apenas a opção classificada.
        - Você não deve responder mensagens em qualquer outro formato que não seja APENAs a classificação da intenção. 
        - O output deve ser APENAS uma das intenções listadas acima.
        """
    )
    return create_agent(
        model=base_model,
        tools=[],
        system_prompt=system_prompt
    )
