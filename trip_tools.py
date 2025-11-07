#pip install -q crewai[tools]==0.120.1 langchain-tavily duckduckgo-search weasyprint markdown2
#pip install -q streamlit python-dotenv


# Importa o decorador `tool` da biblioteca crewai, que transforma funções comuns em "ferramentas"
# que podem ser usadas por agentes de IA (Agents) dentro do ecossistema CrewAI.
from crewai.tools import tool

# Importa a classe TavilySearch, que permite realizar buscas estruturadas na web
# utilizando a API do Tavily (um mecanismo de busca orientado a IA).
from langchain_tavily import TavilySearch

# Importa o DuckDuckGoSearchResults, ferramenta que executa buscas na internet
# usando o mecanismo de busca DuckDuckGo.
from langchain_community.tools import DuckDuckGoSearchResults


# Define uma classe que agrupa ferramentas de busca na internet.
class SearchTools:
    # Cria um método decorado com @tool, que indica ao CrewAI que esta função
    # é uma ferramenta nomeada "Pesquisa na internet".
    @tool("Pesquisa na internet")
    def search_tavily(query: str = "") -> str:
        """
        Função que realiza buscas na internet usando a API Tavily.
        Ideal para obter informações mais recentes e estruturadas.
        """
        # Instancia o objeto TavilySearch, limitando o número máximo de resultados a 4.
        search_tavily = TavilySearch(max_results=4)
        # Executa a busca com base no termo (query) fornecido como argumento.
        search_res = search_tavily.invoke(query)
        # Retorna o resultado da busca (normalmente uma lista ou texto estruturado).
        return search_res

    # Cria uma segunda ferramenta para pesquisa, agora utilizando o DuckDuckGo.
    @tool("Pesquisa na internet com DuckDuckGo")
    def search_duckduckgo(query: str):
        """
        Função que realiza uma busca na web usando o DuckDuckGo.
        Retorna uma lista de resultados de pesquisa.
        """
        # Cria uma instância do mecanismo de busca DuckDuckGo,
        # limitando também a 4 resultados e ativando o modo verboso (debug detalhado).
        search_tool = DuckDuckGoSearchResults(num_results=4, verbose=True)
        # Executa a busca com o termo especificado e retorna os resultados.
        return search_tool.run(query)


# Define uma classe para ferramentas de cálculo matemático.
class CalculatorTools:
    # Declara o método como uma ferramenta CrewAI, nomeada "Faça um cálculo".
    @tool("Faça um cálculo")
    def calculate(operation):
        """
        Realiza cálculos matemáticos básicos.
        Pode ser usado para somas, subtrações, multiplicações e divisões.
        Exemplo de entrada: '200*7' ou '5000/2*10'
        """
        try:
            # Usa a função `eval()` do Python para avaliar a expressão matemática passada como string.
            # Exemplo: eval("5*2+10") → retorna 20.
            return eval(operation)
        except SyntaxError:
            # Caso a expressão não seja válida (erro de sintaxe), retorna uma mensagem de erro amigável.
            return "Erro: Sintaxe inválida"
