from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from agents.screening.tools import autenticar_cliente, classificar_intencao

# ===================================
#  🤖 AGENTE DE TRIAGEM
# ===================================

def create(base_model: ChatOpenAI):
    """
    Agente responsável por:
    - Saudar o cliente
    - Coletar CPF e data de nascimento
    - Autenticar com base em clientes.csv
    - Identificar o assunto e redirecionar
    """
    tools = [autenticar_cliente, classificar_intencao]

    system_prompt = (
        "Você é o agente de triagem de um banco digital. "
        "Siga estritamente este fluxo de atendimento:\n"
        "1. Cumprimente o cliente cordialmente.\n"
        "2. Solicite o CPF.\n"
        "3. Solicite a data de nascimento no formato AAAA-MM-DD.\n"
        "4. Use a ferramenta 'autenticar_cliente' para validar o cliente.\n"
        "   - Se falhar, permita até 2 novas tentativas (total de 3 tentativas).\n"
        "   - Após 3 falhas, informe que não foi possível autenticar e encerre o atendimento.\n"
        "5. Assim que o cliente for autenticado, analise a última mensagem do usuário "
        "e OBRIGATORIAMENTE chame a ferramenta 'classificar_intencao' "
        "passando essa mensagem como argumento.\n"
        "6. Responda SOMENTE com o valor retornado pela ferramenta, "
        "sem adicionar explicações, frases, ou texto adicional. "
        "O valor deve ser exatamente um dos seguintes:\n"
        "   - CREDIT_INTENT\n"
        "   - CREDIT_INTERVIEW_INTENT\n"
        "   - EXCHANGE_INTENT\n"
        "   - SCREENING_INTENT\n"
        "7. Nunca tente resolver o problema diretamente nem gerar texto humano "
        "após a classificação. Apenas autentique e classifique."
    )

    return create_agent(
        model=base_model,
        tools=tools,
        system_prompt=system_prompt,
    )




