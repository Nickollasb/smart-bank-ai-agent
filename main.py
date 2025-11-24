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
        self.document = None
        self.birth_date = None
        self.customer_name = None
        self.score = None
        self.credit_limit = None


class SessionState:
    def __init__(self):
        self.session_id = uuid.uuid4()
        self.is_auth = False
        self.customer = Customer()
        self.active_agent = "screening"
        self.flow = None 
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
        self.conversation_history = [{
            "role": "system",
            "content": f"""
Você é um agente virtual do Banco Ágil.

INSTRUÇÕES GERAIS:
- Atue sempre como um atendente bancário profissional.
- Mantenha linguagem cordial, clara e objetiva.
- Responda de forma natural e humana, evitando robidez excessiva.

BOAS-VINDAS:
- Sempre cumprimente o cliente com “Bom dia”, “Boa tarde” ou “Boa noite”, conforme o horário.
- Apresente-se dando boas-vindas ao atendimento do Banco Ágil

REGRAS DE INTERAÇÃO:
- O atendimento deve fluir naturalmente, sem o cliente perceber qualquer troca de agente.
- Cada resposta deve considerar o contexto recente da conversa.
- Nunca saia do escopo bancário ou forneça informações fora do domínio do banco.
- Não use emojis

DADOS INTERNOS:
- Horário atual: '{get_current_datetime()}'.
- Tentativas máximas de autenticação permitidas: {self.MAX_AUTH_ATTEMPTS}.
- Use estas informações apenas como contexto para definir comportamento, jamais as exponha diretamente ao cliente (exceto o cumprimento baseado no horário).

OBJETIVO:
- Identificar a intenção do cliente e direcionar internamente para o agente especializado (triagem, crédito, entrevista de crédito, câmbio ou conversação geral), mantendo a transição imperceptível.
        """
        }]

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
                self.state.active_agent = "credit"
                self.state.flow = "credit_flow"

            case _:
                self.state.active_agent = "router"
                self.state.flow = None

        return True

    def send(self, user_input: str) -> list[dict]:
        """
        Orquestra o fluxo entre router e agentes especializados.
        Regras gerais:
        - Se não autenticado → sempre vai para screening.
        - Se active_agent for 'interview' → prioriza fluxo da entrevista.
        - Caso contrário → router decide o próximo agente.
        """

        # Injeta dados de contexto na conversa para garantir consistência
        self.conversation_history.append({
            "role": "system",
            "content": (
                f"CPF: {self.state.customer.document}\n"
                f"DATA_NASCIMENTO: {self.state.customer.birth_date}"
            )
        })

        # Captura e armazena dados da autenticação
        cpf_match = re.search(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", user_input)
        if cpf_match:
            self.state.customer.document = cpf_match.group()

        birth_match = re.search(r"\b\d{2}\/?\d{2}\/?\d{4}\b", user_input)
        if birth_match:
            self.state.customer.birth_date = birth_match.group()

        # Adiciona mensagem do usuário ao histórico
        self.conversation_history.append({"role": "user", "content": user_input})

        # FLUXO NÃO AUTENTICADO
        if not self.state.is_auth:
            result = self.agents["screening"].invoke({"messages": self.conversation_history})
            msg = result["messages"][-1].content
            self.conversation_history.append({"role": "assistant", "content": msg})

            if msg.strip() == "AUTH_OK":
                self.state.is_auth = True
                self.conversation_history.append({
                    "role": "system",
                    "content": "AUTENTICADO=True. Redirecionar para router nas próximas mensagens."
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": "Obrigado pela validação, já encontrei os seus dados. Como posso te ajudar?"
                })

            return self.conversation_history

        # FLUXO AUTENTICADO
        # Tratativa de loop para o loop de perguntas da entrevista
        if self.state.active_agent == "interview":
            result = self.agents["interview"].invoke({"messages": self.conversation_history})
            raw_msg = result["messages"][-1].content

            if "END_CREDIT_INTERVIEW" in raw_msg:
                # Remove da mensagem o comando 'END_CREDIT_INTERVIEW' para a LLM
                visible = raw_msg.replace("END_CREDIT_INTERVIEW", "").strip()
                if visible:
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": visible
                    })

                # Marca no histórico interno que a entrevista terminou
                self.conversation_history.append({
                    "role": "system",
                    "content": "END_CREDIT_INTERVIEW"
                })

                # Atualiza estado de fluxo para agente de crédito
                self.handle_intent("END_CREDIT_INTERVIEW")

                # Chama o agente de crédito para usar o novo score e avaliar o limite
                result_credit = self.agents[self.state.active_agent].invoke(
                    {"messages": self.conversation_history}
                )
                credit_msg = result_credit["messages"][-1].content

                self.conversation_history.append({
                    "role": "assistant",
                    "content": credit_msg
                })
                print(f"[{self.state.active_agent}]")
                return self.conversation_history

            self.conversation_history.append({
                "role": "assistant",
                "content": raw_msg
            })

            return self.conversation_history

        # Fluxo de roteamento padrão 
        self.state.active_agent = "router"

        router_result = self.agents["router"].invoke({"messages": self.conversation_history})
        raw_intent = router_result["messages"][-1].content.strip()

        # Sanitiza: remove caracteres estranhos da intent, deixa só A-Z e underscore
        intent = re.sub(r"[^A-Z_]", "", raw_intent)

        # Ajusta estado interno de acordo com a intenção
        self.handle_intent(intent)

        # Chama agente definido pela intent dclassificada pelo router
        result_agent = self.agents[self.state.active_agent].invoke({"messages": self.conversation_history})
        agent_msg = result_agent["messages"][-1].content

        self.conversation_history.append({
            "role": "assistant",
            "content": agent_msg
        })

        return self.conversation_history