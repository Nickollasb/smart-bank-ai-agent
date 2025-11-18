from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

from router.intent_router import global_intent_router
from agents.screening.agent import create as create_screening_agent
from agents.exchange.agent import create as create_exchange_agent
from agents.credit.agent import create as create_credit_agent
# from agents.credit_interview.tools import calculate_new_score, update_new_score

load_dotenv()

# os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

### Cria o modelo de base
base_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY"),
    verbose=True
)

### Cria os agentes
# agent_router = create_router_agent(base_model)
agent_screening = create_screening_agent(base_model)
agent_exchange = create_exchange_agent(base_model)
agent_credit = create_credit_agent(base_model)


autenticado = True
tentativas = 0
MAX_TENTATIVAS = 3

conversation_history = [{"role": "system", "content": "Iniciando atendimento bancário."}]

def extract_intent_from_response(response_text: str) -> str:
    intents = {
        "EXCHANGE_INTENT": "exchange",
        "CREDIT_INTENT": "credit",
        "CREDIT_INTERVIEW_INTENT": "interview",
        "SCREENING_INTENT": "screening",
        "AUTH_FLOW": "authentication",
        "SMALL_TALK": "small_talk",
        "END_CONVERSATION": "end_conversation",
        "UNKNOWN": "unknown"
    }
    
    for key, val in intents.items():
        if key in response_text.upper():
            return val
    return "small_talk"

if __name__ == "__main__":
    print("🤖 Chatbot Financeiro Multi-Agente (POC)")
    print("Digite 'sair' para encerrar.\n")

    while True:
        user_input = input("Você: ").strip()
        # if user_input.lower() == "sair":
        #     print("Encerrando o chatbot...")
        #     break

        conversation_history.append({"role": "user", "content": user_input})

        # --- 🧩 Autenticação ---
        # if not autenticado:
        #     result = agent_screening.invoke({"messages": conversation_history})
        #     resposta = result["messages"][-1].content
        #     print("Agente:", resposta)
        #     conversation_history.append({"role": "assistant", "content": resposta})

        #     if resposta == "AUTH_OK":
        #         autenticado = True
        #         tentativas = 0
        #         print("\n✅ Autenticação confirmada! Vamos continuar.\n")
        #         continue
        #     elif "falha" in resposta.lower() or "incorret" in resposta.lower():
        #         tentativas += 1
        #         if tentativas >= MAX_TENTATIVAS:
        #             print("\n❌ Não foi possível autenticar após 3 tentativas.")
        #             print("Agente: Encerrando o atendimento por segurança.\n")
        #             break
        #         else:
        #             print(f"\n⚠️ Tentativa {tentativas}/{MAX_TENTATIVAS} — tente novamente.\n")
        #             continue
        #     else:
        #         continue
            
        intent = global_intent_router(base_model, user_input)

        # --- 🎯 Pós-autenticação ---
        # result = agent_screening.invoke({"messages": conversation_history})
        # resposta = result["messages"][-1].content
        # conversation_history.append({"role": "assistant", "content": resposta})

        # 🔍 Extrai intenção
        next_agent = extract_intent_from_response(intent)

       
        match next_agent:
            case "exchange":
                agent_result = agent_exchange.invoke({
                    "messages": [{"role": "user", "content": user_input}]
                })
                response = agent_result["messages"][-1].content
                print("Agente de Câmbio:", response)

            case "credit":
                agent_result = agent_credit.invoke({
                    "messages": [{"role": "user", "content": user_input}]
                })
                response = agent_result["messages"][-1].content
                print("Agente de Crédito: ", response)

            case "interview":
                print("Agente de Entrevista de Crédito: Vamos iniciar a sua entrevista de crédito.")
                
            case "end_conversation":
                print("Agente: Foi um prazer ajudar você! Até a próxima.")

            case _:
                ###small_talks case
                print("Agente: Vamos manter a conversa leve! Como posso ajudar você hoje?")
        print("-" * 50)
