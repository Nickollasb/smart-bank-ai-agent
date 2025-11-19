from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

from router.intent_router import global_intent_router
from agents.screening.agent import create as create_screening_agent
from agents.exchange.agent import create as create_exchange_agent
from agents.credit.agent import create as create_credit_agent
from agents.credit_interview.agent import create as create_credit_interview_agent
from agents.general.agent import general_intent_agent

from providers import get_current_datetime

import warnings
warnings.filterwarnings(
    action="ignore",
    message=".*Pydantic V1 functionality isn't compatible with Python 3.14.*"
)

load_dotenv()

# os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


base_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY"),
    verbose=True
)

### Cria os agentes
# agent_router = create_router_agent(base_model)
# agent_screening = create_screening_agent(base_model)
# agent_exchange = create_exchange_agent(base_model)
# agent_credit = create_credit_agent(base_model)

agents = {
    "screening": create_screening_agent(base_model),
    "credit": create_credit_agent(base_model),
    "credit_interview": create_credit_interview_agent(base_model),
    "exchange": create_exchange_agent(base_model)
}

autenticado = False
tentativas = 0
MAX_TENTATIVAS = 3
active_agent = "screening"
conversation_history = []

initial_context = f""""
    Contexto (C):
    - Você é um agente bancário do 'Banco Ágil'.

    Objetivo (O):
    - Seu objetivo é atender os clientes do 'Banco Ágil' a utilizarem os serviços bancários, 
      direcionando o cliente  para conversar com o agente correto, de acordo com a solicitação.
    
    Estilo (S):
    - Atendimento bancário.
    
    Tom(T)
    - Cordial, com linguagem simples/objetiva sempre mantendo o tom profissional.
    
    Audiência(A)
    - Clientes do 'Banco Ágil'.
    
    Formato de resposta (R)
    - Responda sempre o cliente de acordo com o contexto da conversa e/ou solicitação.

    Informações adicionais:
    - Os redirecionamentos entre os agentes devem ser realizados sempre de forma implícita, ou seja, o cliente não pode perceber
      que está sendo direcionado para um agente diferente. A conversa deve fluir naturalmente como se fosse com um humano.
    - Nenhum agente pode atuar fora do seu escopo definido.
    - Você deve saudar o cliente sempre com um 'Bom dia/Boa tarde/Boa noite'. Horário atual para referência: '{get_current_datetime}'
"""

conversation_history = [{"role": "system", "content": "Iniciando atendimento bancário."}]

# def extract_intent_from_response(response_text: str) -> str:
#     intents = {
#         "EXCHANGE_INTENT": "exchange",
#         "CREDIT_INTENT": "credit",
#         "CREDIT_INTERVIEW_INTENT": "credit_interview",
#         "SCREENING_INTENT": "screening",
#         "AUTH_FLOW": "authentication",
#         "SMALL_TALK": "small_talk",
#         "UNKNOWN": "unknown"
#     }
    
#     for key, val in intents.items():
#         if key in response_text.upper():
#             return val
#     return "small_talk"

def handle_intent(intent: str):
    global active_agent

    if intent == "INTENT_CREDIT":
        active_agent = "credit"
        return True

    if intent == "START_INTERVIEW":
        active_agent = "interview"
        return True

    if intent == "FINISH":
        active_agent = "screening"
        return True

    return False

if __name__ == "__main__":
    while True:
        user_input = input("Você: ")

        conversation_history.append({"role": "user", "content": user_input})

        result = agents[active_agent].invoke({"messages": conversation_history})
        resposta = result["messages"][-1].content
        print(f"{active_agent.upper()}: {resposta}")

        conversation_history.append({"role": "assistant", "content": resposta})

        # --- ver se agente pediu troca ---
        if handle_intent(resposta.strip()):
            print(f"🔁 Mudando para agente: {active_agent}")
            conversation_history = []  # reset ou não, dependendo da estratégia

# if __name__ == "__main__":
#     print("🤖 Chatbot Financeiro Multi-Agente (POC)")
#     print("Digite 'sair' para encerrar.\n")

#     while True:
#         user_input = input("-> Eu: ").strip()
#         # if user_input.lower() == "sair":
#         #     print("Encerrando o chatbot...")
#         #     break

#         conversation_history.append({"role": "user", "content": user_input})

#         # --- 🧩 Autenticação ---
#         # if not autenticado:
#         #     result = agent_screening.invoke({"messages": conversation_history})
#         #     resposta = result["messages"][-1].content
#         #     print("Agente:", resposta)
#         #     conversation_history.append({"role": "assistant", "content": resposta})

#         #     if resposta == "AUTH_OK":
#         #         autenticado = True
#         #         tentativas = 0
#         #         print("\n✅ Autenticação confirmada! Vamos continuar.\n")
#         #         continue
#         #     elif "falha" in resposta.lower() or "incorret" in resposta.lower():
#         #         tentativas += 1
#         #         if tentativas >= MAX_TENTATIVAS:
#         #             print("\n❌ Não foi possível autenticar após 3 tentativas.")
#         #             print("Agente: Encerrando o atendimento por segurança.\n")
#         #             break
#         #         else:
#         #             print(f"\n⚠️ Tentativa {tentativas}/{MAX_TENTATIVAS} — tente novamente.\n")
#         #             continue
#         #     else:
#         #         continue
            
#         intent = global_intent_router(base_model, user_input)

#         # --- 🎯 Pós-autenticação ---
#         # result = agent_screening.invoke({"messages": conversation_history})
#         # resposta = result["messages"][-1].content
#         # conversation_history.append({"role": "assistant", "content": resposta})

#         # 🔍 Extrai intenção
#         next_agent = extract_intent_from_response(intent)

#         match next_agent:
#             case "credit":
#                 agent_result = agent_credit.invoke({
#                     "messages": [{"role": "user", "content": user_input}]
#                 })
#                 response = agent_result["messages"][-1].content
#                 conversation_history.append({"role": "assistant", "content": response})
#                 print("-> Agente de Crédito: ", response)

#             case "exchange":
#                 agent_result = agent_exchange.invoke({
#                     "messages": [{"role": "user", "content": user_input}]
#                 })
#                 response = agent_result["messages"][-1].content
#                 conversation_history.append({"role": "assistant", "content": response})
#                 print("-> Agente de Câmbio:", response)

#             case "credit_interview":
#                 response = "Vamos iniciar a sua entrevista de crédito."
#                 conversation_history.append({"role": "assistant", "content": response})
#                 print("-> Agente de Entrevista de Crédito: ", response)

#             case _:
#                 agent_result = general_intent_agent(base_model, conversation_history)
#                 response = agent_result
#                 conversation_history.append({"role": "assistant", "content": response})
#                 print("-> Agente Geral: ", response)
