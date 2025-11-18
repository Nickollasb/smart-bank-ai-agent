from langchain_openai import ChatOpenAI
    
def general_intent_agent(base_model: ChatOpenAI, mensagem: str) -> str:
    """
    Responde o usuário de forma humana, direcionando a conversa para o contexto bancário.
    """
    prompt = f"""
    Responda a seguinte mensagem de forma humana, limitando o cliente ao contexto de serviços da instituição.

    Mensagem do usuário:
    {mensagem}
    
    Responda apenas a mensagem que o cliente deve receber.
    """

    response = base_model.invoke(prompt)
    return response.content.strip()
