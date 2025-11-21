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

os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

class Customer:
    def __init__(self):
        self.document = None
        self.birth_date = None
        self.customer_name = None
        self.score = None
        self.credit_limit = None

class SessionState:
    def __init__(self):
        self.session_id = uuid.uuid8()
        self.is_auth = False
        self.customer = Customer()
        self.active_agent = "screening"
        self.new_try_timeout = None


class AgentController:
    def __init__(self):

        self.active_agent = "screening"
        
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

        self.initial_context = f""""
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
            - Quantidade de tentativas de autenticação permitidas {self.MAX_AUTH_ATTEMPTS}
        """

        self.conversation_history = [{"role": "system", "content": f"Iniciando atendimento bancário. É permitido apenar um total de {self.MAX_AUTH_ATTEMPTS} tentativas de autenticação"}]

    def handle_intent(self, intent: str):        
        match intent:            
            case "CREDIT_INTENT": 
                self.active_agent = "credit"
            case "CREDIT_INTERVIEW_INTENT": 
                self.active_agent = "interview"
            case "EXCHANGE_INTENT": 
                self.active_agent = "exchange"
            case "SMALL_TALK": 
                self.active_agent = "small_talk"
            case _:
                self.active_agent = "router"
        return True
    

    def debug_in(text):
        print("\n>>> TEXTO ENVIADO PARA A LLM:", text)
        return text


    def send(self, user_input: str, conversation_history: list[dict]) -> list[dict]:
        self.conversation_history.append({"role": "user", "content": user_input})

        #TODO: colocar um limite te tempo de 10 min pra tentar novament após todas as tentativas falharem
        # SE NÃO ESTIVER AUTENTICADO
        if not self.is_auth:
            self.result = self.agents["screening"].invoke({"messages": self.conversation_history})
            self.message = self.result["messages"][-1].content
            self.conversation_history.append({"role": "assistant", "content": self.message})
            
            if self.message == "AUTH_OK":
                self.is_auth = True
                self.conversation_history.append({"role": "system", "content": f"""
                    AUTENTICADO={self.state.is_auth}
                    CPF={self.state.customer.document}
                    DATA DE NASCIMENTO={self.state.customer.birth_date}
                    Direcionando agente para o router"""})
                self.message = "Obrigado pela validação, já encontrei os seus dados. Como posso te ajudar?"
                self.conversation_history.append({"role": "assistant", "content": self.message})
            
            return self.conversation_history
              

        # SE ESTIVER AUTENTICADO
        self.active_agent = "router"
        self.result = self.agents[self.active_agent].invoke({"messages": conversation_history})
        self.message = self.result["messages"][-1].content

        if self.handle_intent(self.message.strip()):
            self.result = self.agents[self.active_agent].invoke({"messages": conversation_history})
            self.message = self.result["messages"][-1].content
            self.conversation_history.append({"role": "assistant", "content": self.message})
            return self.conversation_history

   