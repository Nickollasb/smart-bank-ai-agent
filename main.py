import os
import uuid

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from agents.router.agent import create as create_router_agent
from agents.screening.agent import create as create_screening_agent
from agents.exchange.agent import create as create_exchange_agent
from agents.credit.agent import create as create_credit_agent
from agents.credit_interview.agent import create as create_credit_interview_agent
from agents.general.agent import create as create_small_talk_agent

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

class Customer:
    def __init__(self):
        self.document = None
        self.birth_date = None
        self.customer_name = None
        self.score = None
        self.credit_limit = None

    @property
    def document(self):
        return self.document
    
    @document.setter
    def set_customer_document(self, value: str):
        self.document = value

class SessionState:
    def __init__(self):
        self.session_id = uuid.uuid8()
        self.is_auth = False
        self.customer = Customer()
        self.active_agent = "screening"



class AgentController:
    def __init__(self):
        
        self.base_model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            api_key=os.getenv("OPENAI_API_KEY"),
            verbose=True
        )

        self.agents = {
            "router": create_router_agent(self.base_model),
            "screening": create_screening_agent(self.base_model),
            "credit": create_credit_agent(self.base_model),
            "interview": create_credit_interview_agent(self.base_model),
            "exchange": create_exchange_agent(self.base_model),
            "small_talk": create_small_talk_agent(self.base_model)
        }

        self.state = SessionState()

        self.is_auth = False
        self.MAX_AUTH_ATTEMPTS = 2
        self.active_agent = "screening"
        self.conversation_history = []

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
            - Quantidade de tentativas de autenticação permitidas {MAX_AUTH_ATTEMPTS}
        """

        conversation_history = [{"role": "system", "content": f"Iniciando atendimento bancário. É permitido apenar um total de {MAX_AUTH_ATTEMPTS} tentativas de autenticação"}]

        def handle_intent(intent: str):
            global active_agent
            
            match intent:            
                case "CREDIT_INTENT": 
                    active_agent = "credit"
                case "CREDIT_INTERVIEW_INTENT": 
                    active_agent = "interview"
                case "EXCHANGE_INTENT": 
                    active_agent = "exchange"
                case "SMALL_TALK": 
                    active_agent = "small_talk"
                case _:
                    active_agent = "router"
            
            return True



        if __name__ == "__main__":
            print(">>>> Iniciando agente Banco Ágil <<<<\n\n")

            while True:
                user_input = input(" --> Eu: ").strip()
                conversation_history.append({"role": "user", "content": user_input})

                #TODO: colocar um limite te tempo de 10 min pra tentar novament após todas as tentativas falharem
                if not is_auth:
                    result = agents["screening"].invoke({"messages": conversation_history})
                    message = result["messages"][-1].content
                    conversation_history.append({"role": "assistant", "content": message})
                    print(f" ----> [{is_auth}]{active_agent.upper()}: {message}")
                    
                    if message == "AUTH_OK":
                        is_auth = True
                        print(f">>> {is_auth} <<<")
                        conversation_history.append({"role": "system", "content": f"Cliente autenticado: {is_auth}. Direcionando agente para o router"})
                        message = f" ----> [{is_auth}]{active_agent.upper()}: Obrigado pela validação, já encontrei os seus dados. Como posso te ajudar?"
                        conversation_history.append({"role": "assistant", "content": message})
                        print(message)
                        continue
                    else:
                        continue


                active_agent = "router"
                print("<<< entrando no ROUTER >>>")
                result = agents[active_agent].invoke({"messages": conversation_history})
                message = result["messages"][-1].content


                    


                # intent_response = agents[active_agent].invoke({"messages": conversation_history})
                # message = intent_response["messages"][-1].content
                # conversation_history.append({"role": "assistant", "content": message})


                ### SE ESTIVER AUTENTICADO
                if handle_intent(message.strip()):
                    print(f"🔁 Mudando para agente: {active_agent}")

                    
                    # if active_agent != "small_talk":
                    result = agents[active_agent].invoke({"messages": conversation_history})
                    message = result["messages"][-1].content
                    conversation_history.append({"role": "assistant", "content": message})
                    print(f" ----> [{is_auth}]{active_agent.upper()}: {message}")
                    continue
            
                    # result = general_intent_agent(base_model, user_input)
                    # message = result
                    # conversation_history.append({"role": "assistant", "content": message})
                    # print(f" ----> [{is_auth}]{active_agent.upper()}: {message}")


                

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
