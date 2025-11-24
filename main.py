# import os, uuid, re

# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI

# from agents.router.agent import create as create_router_agent
# from agents.screening.agent import create as create_screening_agent
# from agents.exchange.agent import create as create_exchange_agent
# from agents.credit.agent import create as create_credit_agent
# from agents.credit_interview.agent import create as create_credit_interview_agent
# from agents.general.agent import create as create_small_talk_agent

# from providers import get_current_datetime

# load_dotenv()

# os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


# class Customer:
#     def __init__(self):
#         self.document = "05613638110"# None
#         self.birth_date = "26/01/1996" # None
#         self.customer_name = None
#         self.score = None
#         self.credit_limit = None


# class SessionState:
#     def __init__(self):
#         self.session_id = uuid.uuid8()
#         self.is_auth = True # False
#         self.customer = Customer()
#         self.active_agent = "screening"
#         self.new_try_timeout = None


# class AgentController:
#     def __init__(self):
#         self.base_model = ChatOpenAI(
#             model="gpt-4o-mini",
#             temperature=0.1,
#             api_key=os.getenv("OPENAI_API_KEY"),
#             verbose=True
#         )

#         self.agents = {
#             "router": create_router_agent(self.base_model),
#             "screening": create_screening_agent(self.base_model),
#             "credit": create_credit_agent(self.base_model),
#             "interview": create_credit_interview_agent(self.base_model),
#             "exchange": create_exchange_agent(self.base_model),
#             "small_talk": create_small_talk_agent(self.base_model)
#         }

#         self.state = SessionState()

#         self.MAX_AUTH_ATTEMPTS = 2
#         self.conversation_history = []

#         self.initial_context = f"""
#             Contexto (C):
#             - Você é um agente bancário do 'Banco Ágil'.

#             Objetivo (O):
#             - Seu objetivo é atender os clientes do 'Banco Ágil' a utilizarem os serviços bancários, 
#             direcionando o cliente  para conversar com o agente correto, de acordo com a solicitação.
            
#             Estilo (S):
#             - Atendimento bancário.
            
#             Tom(T)
#             - Cordial, com linguagem simples/objetiva sempre mantendo o tom profissional.
            
#             Audiência(A)
#             - Clientes do 'Banco Ágil'.
            
#             Formato de resposta (R)
#             - Responda sempre o cliente de acordo com o contexto da conversa e/ou solicitação.

#             Informações adicionais:
#             - Os redirecionamentos entre os agentes devem ser realizados sempre de forma implícita, ou seja, o cliente não pode perceber
#             que está sendo direcionado para um agente diferente. A conversa deve fluir naturalmente como se fosse com um humano.
#             - Nenhum agente pode atuar fora do seu escopo definido.
#             - Você deve saudar o cliente sempre com um 'Bom dia/Boa tarde/Boa noite'. Horário atual para referência: '{get_current_datetime}'
#             - Quantidade de tentativas de autenticação permitidas {self.MAX_AUTH_ATTEMPTS}
#         """

#         self.conversation_history = [
#             {"role": "system", "content": f"Iniciando atendimento bancário. É permitido apenar um total de {self.MAX_AUTH_ATTEMPTS} tentativas de autenticação"}]

#     def handle_intent(self, intent: str):
#         match intent:
#             case "CREDIT_INTENT":
#                 self.active_agent = "credit"
#             case "CREDIT_INTERVIEW_INTENT":
#                 self.active_agent = "interview"
#             case "EXCHANGE_INTENT":
#                 self.active_agent = "exchange"
#             case "SMALL_TALK":
#                 self.active_agent = "small_talk"
#             case _:
#                 self.active_agent = "router"
#         return True

#     def send(self, user_input: str, conversation_history: list[dict]) -> list[dict]:
#         regex_document = r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"
#         regex_birth_date = r"\b\d{2}\/?\d{2}\/?\d{4}\b"

#         # captura CPF
#         if not self.state.customer.document:
#             match = re.search(regex_document, user_input)
#             if match:
#                 self.state.customer.document = match.group()

#         # captura data de nascimento
#         if not self.state.customer.birth_date:
#             match = re.search(regex_birth_date, user_input)
#             if match:
#                 self.state.customer.birth_date = match.group()

#         self.conversation_history.append(
#             {"role": "user", "content": user_input})

#         # TODO: colocar um limite te tempo de 10 min pra tentar novament após todas as tentativas falharem
#         # SE NÃO ESTIVER AUTENTICADO
#         if not self.state.is_auth:
#             self.result = self.agents["screening"].invoke(
#                 {"messages": self.conversation_history})
#             self.message = self.result["messages"][-1].content
#             self.conversation_history.append(
#                 {"role": "assistant", "content": self.message})

#             if self.message == "AUTH_OK":
#                 self.state.is_auth = True
#                 self.conversation_history.append({"role": "system", "content": f"""
#                     AUTENTICADO={self.state.is_auth}\n\n
#                     Direcionando agente para o router"""})
#                 self.message = "Obrigado pela validação, já encontrei os seus dados. Como posso te ajudar?"
#                 self.conversation_history.append(
#                     {"role": "assistant", "content": self.message})

#             return self.conversation_history

#         # SE ESTIVER AUTENTICADO
#         self.active_agent = "router"
#         self.result = self.agents[self.active_agent].invoke(
#             {"messages": conversation_history})
#         self.message = self.result["messages"][-1].content

#         if self.handle_intent(re.sub('[!@#$]', '', self.message.strip())):
#             self.conversation_history.append(
#                 {"role": "system", "content": f"""
#                     CPF: {self.state.customer.document}
#                     DATA_NASCIMENTO: {self.state.customer.birth_date}
#                 """})
#             print(f"LAST AGENT -> {self.active_agent}")
#             self.result = self.agents[self.active_agent].invoke(
#                 {"messages": conversation_history})
#             self.message = self.result["messages"][-1].content
#             self.conversation_history.append(
#                 {"role": "assistant", "content": f"[{self.active_agent.upper()}]: {self.message}"})
#             self.conversation_history.append(
#                 {"role": "system", "content": f"""
#                     Dados de contexto:
#                     ULTIMO_AGENTE: {self.active_agent}
#                 """})
#             return self.conversation_history


import os, uuid, re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from agents.router.agent import create as create_router_agent
from agents.screening.agent import create as create_screening_agent
from agents.exchange.agent import create as create_exchange_agent
from agents.credit.agent import create as create_credit_agent
from agents.credit_interview.agent import create as create_credit_interview_agent
from agents.general.agent import create as create_small_talk_agent

from providers import get_current_datetime

load_dotenv()

class Customer:
    def __init__(self):
        self.document = "05613638110"
        self.birth_date = "26/01/1996"
        self.customer_name = None
        self.score = None
        self.credit_limit = None


class SessionState:
    def __init__(self):
        self.session_id = uuid.uuid4()
        self.is_auth = True
        self.customer = Customer()
        self.active_agent = "screening"
        self.flow = None      # (credit_request, interview, idle, etc.)
        self.new_try_timeout = None

class AgentController:
    def __init__(self):
        self.base_model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY"),
            verbose=True
        )

        self.agents = {
            "router": create_router_agent(self.base_model),
            "screening": create_screening_agent(self.base_model),
            "credit": create_credit_agent(self.base_model),
            "interview": create_credit_interview_agent(self.base_model),
            "exchange": create_exchange_agent(self.base_model),
            "small_talk": create_small_talk_agent(self.base_model),
        }

        self.state = SessionState()
        self.MAX_AUTH_ATTEMPTS = 2
        self.conversation_history = []

        self.initial_context = f"""
            Você é um agente do Banco Ágil. 
            Siga as regras de atendimento bancário, tom cordial e linguagem objetiva.
            Redirecione entre agentes de forma implícita, sem o cliente perceber.
            Horário atual: '{get_current_datetime}'.
        """

        self.conversation_history.append({
            "role": "system",
            "content": f"Iniciando atendimento bancário com {self.MAX_AUTH_ATTEMPTS} tentativas de autenticação."
        })

    def handle_intent(self, intent: str):
        match intent:
            case "CREDIT_INTENT":
                self.state.active_agent = "credit"
                self.state.flow = "credit_flow"

            case "CREDIT_INTERVIEW_INTENT":
                self.state.active_agent = "interview"
                self.state.flow = "interview_flow"

            case "EXCHANGE_INTENT":
                self.state.active_agent = "exchange"
                self.state.flow = None

            case "SMALL_TALK":
                self.state.active_agent = "small_talk"
                self.state.flow = None

            case "END_CREDIT_INTERVIEW":
                # volta para agente de crédito
                self.state.active_agent = "credit"
                self.state.flow = "credit_flow"

            case _:
                self.state.active_agent = "router"
                self.state.flow = None

        return True


    def send(self, user_input: str, conversation_history: list[dict]) -> list[dict]:

        # Injeção de contexto interno
        conversation_history.append({
            "role": "system",
            "content": f"CPF: {self.state.customer.document}\nDATA_NASCIMENTO: {self.state.customer.birth_date}"
        })
        self.conversation_history = conversation_history

        # Encerramento
        END_KEYWORDS = ["sair", "encerrar", "finalizar", "tchau"]
        if user_input.lower().strip() in END_KEYWORDS:
            self.conversation_history.append({
                "role": "assistant",
                "content": "Certo, estarei aqui caso precise novamente. Até mais!"
            })
            self.state.active_agent = "small_talk"
            self.state.flow = None
            return self.conversation_history

        # Captura automática de CPF e data
        cpf_match = re.search(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", user_input)
        if cpf_match:
            self.state.customer.document = cpf_match.group()

        birth_match = re.search(r"\b\d{2}\/?\d{2}\/?\d{4}\b", user_input)
        if birth_match:
            self.state.customer.birth_date = birth_match.group()

        # Adiciona input do usuário
        self.conversation_history.append({"role": "user", "content": user_input})

        # ====================================================================
        # 1) FLUXO ESPECIAL: aguardando confirmação de entrevista
        # ====================================================================
        # if self.state.flow == "AWAITING_INTERVIEW_CONFIRM":
        #     # Se o usuário respondeu algo afirmativo -> ir direto ao router
        #     self.state.flow = None
        #     self.state.active_agent = "router"

        #     print("[FLOW] Confirmação de entrevista detectada → router")
        #     result = self.agents["router"].invoke({"messages": self.conversation_history})
        #     intent = result["messages"][-1].content.strip()

        #     self.handle_intent(intent)

        #     response = self.agents[self.state.active_agent].invoke(
        #         {"messages": self.conversation_history}
        #     )
        #     msg = response["messages"][-1].content
        #     self.conversation_history.append({"role": "assistant", "content": msg})

        #     return self.conversation_history

        # ====================================================================
        # 2) FLUXOS QUE NÃO DEVEM CHAMAR O ROUTER
        # ====================================================================
        if self.state.active_agent in ["credit", "interview"]:

            result = self.agents[self.state.active_agent].invoke(
                {"messages": self.conversation_history}
            )
            msg = result["messages"][-1].content

            if msg == "START_CREDIT_INTERVIEW":
                self.conversation_history.append({"role": "system", "content": msg})
                self.state.active_agent = 'interview'

                result = self.agents[self.state.active_agent].invoke(
                    {"messages": self.conversation_history}
                )
                msg = result["messages"][-1].content
                # self.state.active_agent = "router"
            
            self.conversation_history.append({"role": "assistant", "content": msg})

            # print(f"[{self.state.active_agent}]")

            # Detecta automaticamente quando o Agente de Crédito ofereceu entrevista
            if "novo score" in msg.lower():
                print('END_CREDIT_INTERVIEW')
                self.conversation_history.append({"role": "system", "content": 'END_CREDIT_INTERVIEW'})
                self.state.active_agent = 'credit'

                result = self.agents[self.state.active_agent].invoke(
                    {"messages": self.conversation_history}
                )
                msg = result["messages"][-1].content

                self.conversation_history.append({"role": "assistant", "content": msg})

            # if self.state.active_agent != 'router':
            return self.conversation_history

        # ====================================================================
        # 3) SENÃO → ROUTER NORMAL
        # ====================================================================
        self.state.active_agent = "router"

        result = self.agents["router"].invoke(
            {"messages": self.conversation_history}
        )
        intent = result["messages"][-1].content.strip()

        self.handle_intent(intent)

        response = self.agents[self.state.active_agent].invoke(
            {"messages": self.conversation_history}
        )
        msg = response["messages"][-1].content

        self.conversation_history.append({"role": "assistant", "content": msg})

        print(f"[{self.state.active_agent}]")
        return self.conversation_history
