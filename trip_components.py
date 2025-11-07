# Importa classes principais da biblioteca CrewAI
# Agent: representa um agente inteligente com um papel e objetivo
# Task: define uma tarefa a ser executada por um agente
# LLM: representa o modelo de linguagem usado pelo agente
from crewai import Agent, Task, LLM

# Importa ferramentas personalizadas criadas no módulo 'trip_tools'
# SearchTools: para realizar buscas externas
# CalculatorTools: para cálculos, como estimativas de custo
from trip_tools import SearchTools, CalculatorTools

# Importa a função dedent, usada para remover indentação extra de textos multilinha
from textwrap import dedent

# Importa módulos para manipular variáveis de ambiente e sistema
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (como chaves de API)
load_dotenv()

# ======================================================
# CLASSE: TripAgents
# Define diferentes agentes com papéis específicos no planejamento de viagem.
# ======================================================
class TripAgents:
    def __init__(self):
        # Inicializa o modelo de linguagem chatgpt, da Openai, com a chave da API.
        # Esse modelo será compartilhado por todos os agentes.
        self.chatgpt = LLM(
            model="gpt-4o-mini",  # Define qual modelo da Openai será usado
            api_key=os.getenv("OPENAI_API_KEY"),  # Busca a chave no arquivo .env
        )

    # --------------------------------------------------
    # Agente 1: Especialista em informações da cidade
    # --------------------------------------------------
    def city_info_agent(self):
        return Agent(
            # Função principal do agente
            role="Especialista em informações da cidade",

            # Objetivo geral do agente
            goal=dedent(
                """Reunir informações úteis sobre o destino escolhido, com base nos interesses e datas da viagem,
                ajudando viajantes a entender o contexto geral do local."""
            ),

            # História de fundo — define a "personalidade" e contexto do agente
            backstory=dedent(
                """
                Sou um especialista com amplo conhecimento sobre cidades ao redor do mundo,
                capaz de fornecer detalhes atualizados sobre clima, eventos culturais, segurança,
                costumes locais e outros aspectos práticos para quem pretende visitar o local.
                Sou apaixonado por compartilhar as melhores experiências e 'joias escondidas' do local.
                """
            ),

            # Modelo de linguagem a ser usado (chatgpt)
            llm=self.chatgpt,

            # Ferramentas auxiliares disponíveis — neste caso, busca por informações
            tools=[SearchTools.search_tavily],

            # Mostra logs detalhados durante a execução
            verbose=True,

            # Número máximo de iterações que o agente pode realizar
            max_iter=10,

            # Impede que o agente delegue sua tarefa a outro agente
            allow_delegation=False,
      )

    # --------------------------------------------------
    # Agente 2: Especialista em logística de viagem
    # --------------------------------------------------
    def logistics_expert_agent(self):
        return Agent(
            role="Especialista em logística de viagem",  # Função do agente
            goal="Identificar as melhores opções logísticas para a viagem, com foco em praticidade, custo-benefício e conforto.",  # Objetivo
            backstory=dedent(
                """
                Sou um profissional focado em planejar a logística da viagem: transporte, hospedagem e deslocamento local.
                Tenho conhecimento sobre companhias aéreas, apps de mobilidade, regiões seguras para se hospedar e otimização de trajetos.
                """
            ),
            llm=self.chatgpt,  # Modelo de linguagem
            tools=[
                SearchTools.search_tavily,  # Ferramenta de busca
                CalculatorTools.calculate   # Ferramenta de cálculo de custos
            ],
            verbose=True,
            max_iter=10,
            allow_delegation=False,
        )

    # --------------------------------------------------
    # Agente 3: Planejador de itinerário personalizado
    # --------------------------------------------------
    def itinerary_planner_agent(self):
        return Agent(
            role="Planejador de itinerário personalizado",
            goal="Criar um roteiro completo com base nas preferências do usuário.",
            backstory=dedent(
                """
                Sou um guia profissional apaixonado por viagens, especialista em organização de itinerários personalizados.
                Minha missão é integrar dados sobre clima, atrações, eventos e logística em uma experiência otimizada para o turista.
                """
            ),
            llm=self.chatgpt,
            tools=[SearchTools.search_tavily],
            verbose=True,
            max_iter=10,
            allow_delegation=False,
        )

    # --------------------------------------------------
    # Agente 4: Guia de idioma e etiqueta local
    # --------------------------------------------------
    def language_guide_agent(self):
        return Agent(
            role="Especialista em comunicação e etiqueta local",
            goal="Gerar um guia traduzido com frases úteis, dicas de etiqueta e expressões práticas com base nas atividades do roteiro.",
            backstory=dedent(
                """
                Sou um especialista em línguas e culturas do mundo.
                Meu trabalho é ajudar turistas a se comunicarem melhor no destino, traduzindo expressões essenciais relacionadas ao roteiro,
                como pedidos em restaurantes, orientações para transporte e interações cotidianas.
                Também forneço dicas culturais para evitar gafes e tornar a experiência mais fluida e respeitosa.
                """
            ),
            llm=self.chatgpt,
            tools=[SearchTools.search_tavily],
            verbose=True,
            max_iter=5,
            allow_delegation=False,
        )


# ======================================================
# CLASSE: TripTasks
# Define as tarefas específicas que cada agente deve executar.
# ======================================================
class TripTasks:
    # --------------------------------------------------
    # Tarefa 1: Coletar informações da cidade
    # --------------------------------------------------
    def city_info_task(self, agent, from_city, destination_city, interests, date_from, date_to):
        return Task(
            # Descrição detalhada da tarefa
            description=dedent(
                f"""
                Levantar informações detalhadas sobre a cidade e coletar dados úteis sobre clima, segurança e costumes locais.
                Identificar marcos culturais, pontos históricos, locais de entretenimento, experiências gastronômicas e quaisquer atividades que se alinhem às preferências do usuário.
                Também destacar eventos e festivais sazonais que podem ser de interesse durante a visita do viajante.
                Use as ferramentas disponíveis para buscar fontes atualizadas e confiáveis.

                Viajando de: {from_city}
                Para: {destination_city}
                Interesses do viajante: {interests}
                Chegada: {date_from}
                Partida: {date_to}

                Seja criterioso, como se estivesse ajudando alguém a ter uma experiência inesquecível.
                """
            ),

            # Saída esperada no formato markdown
            expected_output=dedent(
                f"""
                Um guia detalhado (em formato markdown) em português que inclui:
                - Resumo da cidade e sua cultura;
                - Uma lista selecionada de lugares recomendados para visitar e eventos (se houver);
                - Um detalhamento das despesas diárias, como custos médios com alimentação;
                - Recomendações de segurança;
                - Dicas de costumes locais;
                """
            ),

            # Agente responsável por executar a tarefa
            agent=agent,

            # Nome do arquivo onde o resultado será salvo
            output_file='relatorio_local.md',
        )

    # --------------------------------------------------
    # Tarefa 2: Planejar logística da viagem
    # --------------------------------------------------
    def plan_logistics_task(self, context, agent, destination_city, interests, date_from, date_to):
        return Task(
            description=dedent(
                f"""
                Planejar a logística da viagem.
                Identificar as melhores opções de hospedagem, voos e transporte local considerando:

                Destino: {destination_city}
                Data de chegada: {date_from}
                Data de partida: {date_to}
                Interesses: {interests}

                Avalie preço, localização, conveniência e segurança.
                """
            ),
            expected_output=dedent(
                f"""
                Relatório em português (em formato markdown):
                - Sugestão de hospedagens, preferencialmente com localização estratégica;
                - Opções de voos ou meios de transporte para chegada/partida;
                - Sugestões de deslocamento dentro da cidade;
                - Estimativas de custo para cada item;
                """
            ),
            context=context,  # Contexto anterior (informações da cidade)
            agent=agent,      # Agente responsável
            output_file='relatorio_logistica.md',
        )

    # --------------------------------------------------
    # Tarefa 3: Criar o roteiro da viagem
    # --------------------------------------------------
    def build_itinerary_task(self, context, agent, destination_city, interests, date_from, date_to):
        return Task(
            description=dedent(
                f"""
                Esta tarefa sintetiza todas as informações para criar o roteiro final da viagem.
                Com base nas informações dos outros agentes, desenvolva um itinerário detalhado.
                Cada dia deve conter atividades, clima, transporte, refeições e estimativa de gastos.

                Destino: {destination_city}
                Interesses: {interests}
                Data de chegada: {date_from}
                Data de partida: {date_to}
                """
            ),
            expected_output=dedent("""
                Documento em português que inclui (em formato markdown):
                - Boas vindas e apresentação da cidade em até 2 parágrafos.
                - Programação diária com sugestões de horários e atividades
                - Atrações distribuídas por região e logística
                - Clima previsto, sugestões de transporte e alimentação
                - Eventos e festivais sazonais (se houver)
                - Estimativa de gastos por dia, custo médio das despesas diárias e pontos turísticos.
                - Visão geral dos destaques da cidade com base nas recomendações do guia.
                - Outras dicas e informações adicionais para uma viagem e estadia tranquila.
                """),
            context=context,  # Usa dados das tarefas anteriores
            agent=agent,
            output_file='roteiro_viagem.md',
        )

    # --------------------------------------------------
    # Tarefa 4: Criar guia de idioma e etiqueta local
    # --------------------------------------------------
    def language_guide_task(self, context, agent, destination_city):
        return Task(
            description=dedent(
                f"""
                Com base no destino ({destination_city}) e nas atividades previstas no roteiro, monte um guia traduzido com frases úteis e dicas culturais.
                Deve ser no idioma falado nesse local (ou também em inglês, caso seja uma língua aceitável para ser usada por turistas nesse local).

                Inclua expressões comuns para situações que podem ser úteis, como:
                - Interações em restaurantes (como fazer pedidos, pagar a conta, pedir recomendações);
                - Deslocamento (perguntar por rotas, chamar transporte, entender sinalização);
                - Situações cotidianas (compras, pedidos de ajuda, saudações e agradecimentos);
                - Dicas de etiqueta local que o turista deve saber (gestos, hábitos, regras sociais).

                Use linguagem clara e educativa.

                Considere o seguinte roteiro de viagem:
                '{context}'
                """
            ),
            expected_output=dedent(
                """
                Um mini-guia em português contendo:
                - Lista de frases traduzidas organizadas por situação (restaurantes, transporte, compras, etc.);
                - Dicas de etiqueta e costumes locais;
                - Sugestões de como pronunciar corretamente (quando aplicável);
                - Recomendações práticas para comunicação eficaz no destino.
                """
            ),
            agent=agent,
            output_file='guia_comunicacao.md',
        )
