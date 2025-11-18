from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from agents.screening.tools import autenticar_cliente

def create(base_model: ChatOpenAI):
    """
    Screening Agent — apenas autenticação.
    NÃO tenta classificar intenção.
    NÃO tenta responder assuntos gerais.
    """
    tools = [autenticar_cliente]

    system_prompt = (
        "Você é o agente de triagem de um banco digital.\n"
        "Seu único objetivo é AUTENTICAR o cliente antes de liberá-lo para outros agentes.\n\n"

        "Fluxo:\n"
        "1. Cumprimente.\n"
        "2. Peça o CPF.\n"
        "3. Peça a data de nascimento.\n"
        "4. Use exclusivamente a ferramenta 'autenticar_cliente'.\n"
        "5. Se falhar, permita 3 tentativas.\n"
        "6. Se autenticar, responda APENAS:\n"
        "```AUTH_OK```\n"
        "7. Não responda perguntas sobre câmbio, crédito ou outros assuntos.\n"
        "8. Se o usuário perguntar outras coisas antes da autenticação, diga:\n"
        "   'Vamos concluir sua autenticação primeiro.'\n"
    )

    return create_agent(
        model=base_model,
        tools=tools,
        system_prompt=system_prompt
    )
