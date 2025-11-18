from langchain_openai import ChatOpenAI
from langchain.tools import tool

# def create(base_model: ChatOpenAI):
#     return global_intent_router(base_model)
    
def global_intent_router(base_model: ChatOpenAI, mensagem: str) -> str:
    """
    Classifica a intenção do usuário globalmente.
    Sempre retorna exatamente 1 valor.
    """
    prompt = f"""
    Classifique a intenção da seguinte mensagem em apenas UMA das opções:
    
    - AUTH_FLOW (perguntas relacionadas à autenticação, cadastro, identidade, CPF, data de nascimento, login)
    - EXCHANGE_INTENT (câmbio, dólar, euro, moedas, cotação, forex)
    - CREDIT_INTENT (empréstimo, financiamento, limite, crédito)
    - CREDIT_INTERVIEW_INTENT (avaliação de perfil, entrevista, análise de crédito)
    - END_CONVERSATION (obrigado, valeu, tchau, encerra)
    - SMALL_TALK (cumprimentos, conversa fiada, assuntos gerais)

    Mensagem do usuário:
    {mensagem}

    Responda com apenas uma opção.
    """

    response = base_model.invoke(prompt)
    return response.content.strip()
