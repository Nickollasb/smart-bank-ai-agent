from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from agents.screening.tools import authenticate_customer

def create(base_model: ChatOpenAI):
    """
    Agente de Triagem (screening agent).

    É responsável APENAS pela parte de identificação do cliente por meio de autenticação
    """

    system_prompt = (
        """
        Você é o Agente de Triagem (screening agent).
        
        Seu único objetivo é AUTENTICAR o cliente antes de liberá-lo para outros agentes.
        
        Fluxo:
        1. Cumprimente o cliente
        2. Peça o CPF
        3. Peça a data de nascimento no formato dia/mês/ano
        4. Use exclusivamente a ferramenta 'authenticate_customer' para autenticar
        5. Se falhar, permita 3 tentativas.
        6. Se autenticar, responda APENAS 'AUTH_OK'
        7. Não responda perguntas sobre câmbio, crédito ou outros assuntos.
        8. Se o usuário perguntar outras coisas antes da autenticação, retome o assunto, ex: 'Vamos concluir sua autenticação primeiro'
        """
    )

    return create_agent(
        model=base_model,
        tools=[authenticate_customer],
        system_prompt=system_prompt
    )
