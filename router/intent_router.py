from langchain_openai import ChatOpenAI

def global_intent_router(base_model: ChatOpenAI, user_input: str) -> str:
    """
    Classifica a intenção do usuário globalmente.
    Sempre retorna exatamente 1 valor.
    """

    prompt = f"""
    Classifique a intenção da seguinte mensagem em apenas UMA das opções:
    
    - SMALL_TALK (cumprimentos, conversa fiada, assuntos gerais, despedida e.g "obrigado", "valeu", "tchau", "encerrar")
    - CREDIT_INTENT (limite, solicitar novo limite de crédito, score de crédito)
    - CREDIT_INTERVIEW_INTENT (realiza entrevista com o cliente coletando dados para saber se é possível aumentar seu limite de crédito)
    - EXCHANGE_INTENT (câmbio, dólar, euro, moedas, cotação)

    Mensagem do usuário:
    {user_input}

    Responda com apenas uma opção.
    """

    response = base_model.invoke(prompt)
    return response.content.strip()
