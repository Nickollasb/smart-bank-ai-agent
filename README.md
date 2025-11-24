### Visão Geral do projeto
Agente de IA desenvolvido para o Banco Ágil (nome fictício) com objetivo de autenticar o cliente e em seguida, permitir a consulta/aumento de limite de crédito, realizar entrevista de crédito para aumento de limite e cotação atualizada de moedas estrangeiras para BRL.

### Arquitetura do sistema
O projeto foi desenvolvido com a stack detalhada na seção _"Escolhas técnicas e justificativas"_ por uma maior familiaridade do desenvolvedor com as tecnologias e por serem ferramentas confiáveis para uso em ambiente produtivo.

**O projeto é composto por 2 grandes partes:**
- **Frontend**: Interface com Streamlit em formato de chat que facilita a interação entre o usuário e os Agentes de IA
- **Backend**: Código de estruturação e implementação dos agentes de IA

**O fluxo de implementação da IA foi desenvolvido respeitando o fluxo definido no desafio técnico, onde:**
1. O Agente de Triagem é responsável por funcionar como um guardião da segurança e autenticar o cliente antes de prosseguir com a conversa.
2. Após a autenticação ser realizada com sucesso, o agente segue o fluxo: ```Novo input do usuário -> Roteador classifica intenção -> Direciona para o agente responsável.```
3. Caso o Roteador identifique que o usuário deseja fazer a entrevista, direciona para o Agente de Entrevista de Crédito e o agente faz o loop de perguntas até garantir que todas foram respondidas com sucesso.
4. Com as perguntas de Entrevista de Crédito realizadas, o Agente de Crédito recalcula e informa o novo limite do cliente.

**Os dados do projeto estão na pasta "data", onde temos 3 tabelas (arquivos .csv):**
- **clientes.csv**
  - Tabela principal onde estão salvos os dados de clientes
- **score_limite.csv**
  - Tabela onde estão definidos as janelas de score para a base de cálculo do aumento de score e limite
- **solicitacoes_aumento_limite.csv**
  - Solicitações de aumento de limite (Aprovadas e/ou Reprovadas pelo agente)

### Funcionalidades implementadas.
- **Router**
  - Para servir como classificador das intenções e retirar a responsabilidade do Agente de Triagem (reduzir escopo de responsabilidades).
- **Agente de Triagem**
  - Responsável por realizar a autenticação do cliente com CPF e Data de Nascimento, antes de chamar qualquer outra funcionalidade.
- **Agente de Crédito**
  - Responsável por informar o limite de crédito ao cliente;
  - Responsável por validar se o cliente tem interesse de fazer uma entrevista de crédito e redirecioná-lo para o Agente de Entrevista de Crédito.
- **Agente de Entrevista de Crédito**
  - Realiza uma série de perguntas como faixa de renda, despesas etc, para calcular um novo score de crédito para o cliente.
- **Agente de Câmbio**
  - Realiza cotação atualizada de moedas estrangeiras diversas para BRL (Real Brasileiro)

### Desafios enfrentados e como foram resolvidos
O projeto foi bem desafiador, visto que atuei sempre com ferramentas gráficas pré-configuradas para criação dos agentes (Blip, N8N, etc). Já havia atuado em um projeto anteriormente com Langchain, porém não havia tido a experiência de implementar toda a arquitetura do código do zero.

Para superar os desafios, utilizei muito a documentação das tecnologias para me apoiar. Mesmo não sabendo fazer algo, hoje temos uma vasta quantidade de informação na internet. Basta pesquisar da forma correta.

Um desafio que me chamou atenção foi garantir que os roteamentos estão sendo feitos corretamente entre os agentes. Dentro do prompt, busquei ser o mais claro possível para a LLM saber quando indicar uma troca mais sensível e o que ela precisaria retornar em cada caso.

Apesar disso, o projeto me motivou ainda mais a direcionar os meus estudos para o Langchain e utilizá-lo como stack principal, pois desta forma é possível criar projetos robustos, com mais controle e segurança.

**Pontos de melhoria para a próxima versão do projeto, considerando este desafio técnico como uma POC:**
- Melhorar a observabilidade do projeto (Langsmith)
- Anonimização dos dados pessoais (PII Anonymization)
- Uso de um "resumidor" de contexto para reduzir o uso de tokens (SummarizationMiddleware)
- Desenvolvimento de testes unitários das ferramentas (tools) para garantir a consistência do código implementado durante a evolução do projeto.
- Tratativas mais robustas para as exceções do projeto
- Definir a tonalidade de conversa, de acordo com a preferência da instituição e adaptar o agente para isso. Para este desafio, foi escolhida uma linguagem mais objetiva e profissional.
- Testes e alguns pequenos ajustes para refinamento final

### Escolhas técnicas e justificativas.
A escolha técnica definida baseada dentro da stack técnica sugerida para o projeto.

**LINGUAGEM**
- **Python** (mais utilizada em projetos de IA e com um maior portifólio de ferramentas e bibliotecas para esta finalidade)

**INTERFACE:**
- **Streamlit** (simples de implementar, leve para executar)

**AGENTE DE IA:**
- **Langchain** (stack confiável para projetos em produção)
- **OpenAI API** (familiaridade com a API e os modelos de IA)
- **Modelo de IA** (gpt-4o-mini - mais rápido nas respostas)

### Tutorial de execução e testes.
1. Crie um ambiente virtual para o projeto:
- ```$ python3 -m venv venv```
- ```$ source venv/bin/activate```
2. Instale todas as dependências a partir da raiz do projeto:
- ```$ pip install -r requirements.txt```
3. Após instaladas todas as dependências, insira a chave ```OPENAI_API_KEY=``` no .env e inicie o projeto a partir do comando abaixo:
- ```$ streamlit run chat.py```