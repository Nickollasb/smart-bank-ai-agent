from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

from agents.screening.agent import create as create_screening_agent
from agents.exchange.agent import create as create_exchange_agent

load_dotenv()

base_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY")
)

agent_screening = create_screening_agent(base_model)
agent_exchange = create_exchange_agent(base_model)

autenticado = False
tentativas = 0
MAX_TENTATIVAS = 3

conversation_history = [{"role": "system", "content": "Iniciando atendimento bancário."}]

def extract_intent_from_response(response_text: str) -> str:
    intents = {
        "EXCHANGE_INTENT": "exchange",
        "CREDIT_INTENT": "credit",
        "CREDIT_INTERVIEW_INTENT": "interview",
        "SCREENING_INTENT": "screening"
    }
    for key, val in intents.items():
        if key in response_text.upper():
            return val
    return "screening"

if __name__ == "__main__":
    print("🤖 Chatbot Financeiro Multi-Agente (POC)")
    print("Digite 'sair' para encerrar.\n")

    while True:
        user_input = input("Você: ").strip()
        if user_input.lower() == "sair":
            print("Encerrando o chatbot...")
            break

        conversation_history.append({"role": "user", "content": user_input})

        # --- 🧩 Autenticação ---
        if not autenticado:
            result = agent_screening.invoke({"messages": conversation_history})
            resposta = result["messages"][-1].content
            print("Agente:", resposta)
            conversation_history.append({"role": "assistant", "content": resposta})

            if "sucesso" in resposta.lower() or "autenticação bem-sucedida" in resposta.lower():
                autenticado = True
                tentativas = 0
                print("\n✅ Autenticação confirmada! Vamos continuar.\n")
                continue
            elif "falha" in resposta.lower() or "incorret" in resposta.lower():
                tentativas += 1
                if tentativas >= MAX_TENTATIVAS:
                    print("\n❌ Não foi possível autenticar após 3 tentativas.")
                    print("Agente: Encerrando o atendimento por segurança.\n")
                    break
                else:
                    print(f"\n⚠️ Tentativa {tentativas}/{MAX_TENTATIVAS} — tente novamente.\n")
                    continue
            else:
                continue

        # --- 🎯 Pós-autenticação ---
        result = agent_screening.invoke({"messages": conversation_history})
        resposta = result["messages"][-1].content
        print("Triagem:", resposta)
        conversation_history.append({"role": "assistant", "content": resposta})

        # 🔍 Extrai intenção
        next_agent = extract_intent_from_response(resposta)

        # --- 🔁 Redirecionamento automático ---
        if next_agent == "exchange":
            print("\n🔁 Redirecionando automaticamente para o agente de câmbio...\n")
            exchange_result = agent_exchange.invoke({
                "messages": [{"role": "user", "content": user_input}]
            })
            exchange_response = exchange_result["messages"][-1].content
            print("Agente de Câmbio:", exchange_response)
            print("-" * 50)
            continue

        elif next_agent == "credit":
            print("\n💳 (Em breve) Redirecionamento para o agente de crédito...\n")
        elif next_agent == "interview":
            print("\n🧾 (Em breve) Redirecionamento para o agente de entrevista de crédito...\n")
        else:
            print("Agente: Certo, poderia me dar mais detalhes?")
        print("-" * 50)
