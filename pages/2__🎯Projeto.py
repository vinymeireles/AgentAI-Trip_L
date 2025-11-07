import streamlit as st

st.set_page_config(page_title="Agentes de IA para Turismo", page_icon="🧠", layout="wide")

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

st.sidebar.image("Img/logoAI.png", width=200)


# ======================================
# 🎯 Cabeçalho do Projeto
# ======================================


st.title("🧠 Projeto: Agentes de IA para Turismo")
st.markdown("---")

st.info("""
Solução baseada em **IA Multiagente** para automatizar a criação de roteiros turísticos personalizados, 
melhorando a eficiência das agências e a experiência dos viajantes.
""")

# ======================================
# 🧭 Abas principais do projeto
# ======================================
tabs = st.tabs([
    "🧭 Cenário",
    "⚙️ Desafios",
    "🤖 Solução Multiagente",
    "🎯 Objetivos",
    "💡 Tecnologia e Metodologia",
    "🚀 Resultados Esperados",
    "🗂️ Conclusão"
])

# ======================================
# 🧭 Cenário
# ======================================
with tabs[0]:
    st.header("🧭 Cenário")
    st.markdown("""
    As agências e guias turísticos enfrentam **grande gasto de tempo** na criação de roteiros personalizados 
    para cada cliente.  
    O processo é manual e envolve pesquisa detalhada sobre **atrações, clima, logística, cultura e preferências pessoais**, 
    o que gera **atrasos e ineficiência** no atendimento.
    """)

# ======================================
# ⚙️ Desafios
# ======================================
with tabs[1]:
    st.header("⚙️ Desafios Identificados")
    st.markdown("""
    - 🕒 Montagem manual e demorada de itinerários personalizados  
    - 🧩 Dificuldade em adaptar-se rapidamente ao perfil de cada viajante  
    - 🔁 Necessidade de automatizar tarefas repetitivas de pesquisa e planejamento  
    - 📈 Falta de escalabilidade — equipe precisaria crescer para atender à demanda
    """)

# ======================================
# 🤖 Solução Multiagente
# ======================================
with tabs[2]:
    st.header("🤖 Solução Proposta — Sistema Multiagente com IA")

    st.markdown("""
    Criação de um **guia virtual inteligente** que monta roteiros personalizados com base nas preferências do cliente, 
    utilizando **múltiplos agentes de IA especializados**.
    """)

    with st.expander("👥 Agentes de IA e Funções"):
        st.markdown("""
        1. **Especialista em informações da cidade**  
           → Pesquisa clima, eventos, cultura e atrações locais.  

        2. **Especialista em logística de viagem**  
           → Sugere hospedagens, transportes e voos adequados ao perfil do viajante.  

        3. **Planejador de itinerário personalizado**  
           → Organiza o roteiro completo com previsão do tempo, orçamento e dicas.  

        4. **Especialista em comunicação e etiqueta local**  
           → Cria guias traduzidos e fornece dicas culturais com base nas atividades previstas.
        """)

# ======================================
# 🎯 Objetivos
# ======================================
with tabs[3]:
    st.header("🎯 Objetivos do Projeto")
    st.markdown("""
    - 🤝 Automatizar a geração de **roteiros turísticos personalizados**  
    - ⏱️ Reduzir o tempo e o esforço de planejamento das agências  
    - 💬 Melhorar a experiência do cliente com **respostas rápidas e precisas**  
    - 🧩 Fornecer uma solução **modular, escalável e personalizável**, baseada no framework **CrewAI**
    """)

# ======================================
# 💡 Tecnologia e Metodologia
# ======================================
with tabs[4]:
    st.header("💡 Tecnologia e Metodologia")
    st.markdown("""
    - 🧠 **Framework CrewAI** → Orquestração de múltiplos agentes com papéis definidos  
    - 🔄 **Abordagem ReAct** → Agentes “pensam”, **agem e aprendem por observação** em ciclos  
    - 🤝 **Colaboração entre agentes** → Trabalho em equipe (sequencial ou paralelo)  
    - 🧾 **Integração de ferramentas** → Busca de dados e geração de relatórios automáticos (PDF)
    """)

    with st.expander("📊 Como funciona o ciclo ReAct"):
        st.markdown("""
        1. **Thought (Pensamento):** o agente analisa o contexto e decide o que fazer  
        2. **Action (Ação):** executa uma função com parâmetros específicos  
        3. **Observation (Observação):** analisa o resultado da ação  
        4. Repete o ciclo até considerar a tarefa concluída ✅
        """)

# ======================================
# 🚀 Resultados Esperados
# ======================================
with tabs[5]:
    st.header("🚀 Resultados Esperados")
    st.markdown("""
    A aplicação será capaz de:

    - ⚡ Gerar roteiros personalizados **de forma rápida e automatizada**  
    - 🧱 Permitir **adição de novos agentes e funções**  
    - 💰 **Reduzir custos operacionais** e aumentar a produtividade  
    - 🌍 Oferecer **um diferencial competitivo** com atendimento inteligente e multilíngue
    """)

# ======================================
# 🗂️ Conclusão
# ======================================
with tabs[6]:
    st.header("🗂️ Conclusão")
    st.success("""
    O projeto **Agentes de IA para Turismo** demonstra como **sistemas multiagentes** 
    podem transformar o planejamento de viagens, tornando-o **mais eficiente, escalável e personalizado**, 
    com o suporte de inteligência artificial colaborativa.
    """)
