# ==========================================================
# 🌍 AgentAI Trip - Planejamento de Viagens com IA
# Login
# Usuário padrão: teste | senha: teste
# ==========================================================

import streamlit as st
import sqlite3
import os
import hashlib
import binascii
import hmac
from datetime import datetime
from crewai import Crew, Process
from trip_components import TripAgents, TripTasks
from trip_utils import capture_output
from textwrap import dedent
import time
import markdown2
#from weasyprint import HTML
import io
import shutil
import ctypes.util
import re

# ==========================================================
# CONFIGURAÇÕES INICIAIS
# ==========================================================

DB_PATH = "users.db"
os.environ["LITELLM_LOCAL_CACHE"] = "True"
print(ctypes.util.find_library("gobject-2.0"))

st.set_page_config(page_title="AgentAI Trip", page_icon="🌍", layout="wide")

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.image("Img/logoAI.png", width=200)

# ==========================================================
# FUNÇÕES DE LOGIN / SEGURANÇA
# ==========================================================

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

    # cria admin padrão
    cur.execute("SELECT id FROM users WHERE username='admin'")
    if not cur.fetchone():
        pwd_hash, salt = hash_password('admin123')
        cur.execute(
            "INSERT INTO users (username, password_hash, salt, role, created_at) VALUES (?, ?, ?, ?, ?)",
            ('admin', pwd_hash, salt, 'admin', datetime.utcnow().isoformat())
        )
        conn.commit()
    conn.close()

def hash_password(password: str, salt: bytes = None):
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 200000)
    return binascii.hexlify(dk).decode(), binascii.hexlify(salt).decode()

def verify_password(stored_hash_hex, stored_salt_hex, password_attempt):
    salt = binascii.unhexlify(stored_salt_hex)
    attempt_hash_hex, _ = hash_password(password_attempt, salt)
    return hmac.compare_digest(attempt_hash_hex, stored_hash_hex)

def authenticate_user(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT password_hash, salt, role FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False, "Usuário não encontrado", None
    stored_hash, stored_salt, role = row
    ok = verify_password(stored_hash, stored_salt, password)
    if ok:
        return True, "Autenticado", role
    else:
        return False, "Senha incorreta", None

init_db()

# ==========================================================
# CONTROLE DE SESSÃO
# ==========================================================

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'login_flag' not in st.session_state:
    st.session_state['login_flag'] = False

# ==========================================================
# TELA DE LOGIN
# ==========================================================

if not st.session_state['authenticated']:
    st.title("🔐 Acesso - AgentAI Trip")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar") or st.session_state['login_flag']:
        if not st.session_state['login_flag']:
            ok, msg, role = authenticate_user(username.strip(), password)
            if ok:
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.session_state['role'] = role
                st.session_state['login_flag'] = True
                st.rerun()  # ✅ recarrega imediatamente a página autenticada
            else:
                st.error(msg)
        else:
            st.session_state['login_flag'] = False

    st.stop()

# ==========================================================
# APLICAÇÃO PRINCIPAL (PÓS LOGIN)
# ==========================================================

# --------------------------- SIDEBAR PERSONALIZADA --------------------------- #
st.sidebar.markdown(f"👋 Olá, **{st.session_state.username}**!")

if st.sidebar.button("🚪 Sair"):
    for key in ["authenticated", "username", "role", "login_flag"]:
        st.session_state[key] = False if key == "authenticated" else ""
    st.rerun()

# --------------------------- CONTEÚDO PRINCIPAL --------------------------- #
st.title("🌍 AgentAI Trip")
st.markdown("""
### ✨ Bem-vindo ao seu assistente de viagens com Inteligência Artificial
Aqui você pode:
- 🧭 Planejar itinerários inteligentes
- 🧠 Obter recomendações personalizadas
- 💬 Interagir com agentes de IA para planejamento
- 📜 Criar e acompanhar roteiros de destinos de viagem
""")


# --------------------------- CONFIGURAÇÃO DO APP PRINCIPAL --------------------------- #

OUTPUT_DIR = os.path.join(os.getcwd(), "viagem")
os.makedirs(OUTPUT_DIR, exist_ok=True)

files = {
    "roteiro_viagem.md": "roteiro_viagem.pdf",
    "guia_comunicacao.md": "guia_comunicacao.pdf",
    "relatorio_local.md": "relatorio_local.pdf",
    "relatorio_logistica.md": "relatorio_logistica.pdf"
}

class TripCrew:
    def __init__(self, from_city, destination_city, date_from, date_to, interests):
        self.from_city = from_city
        self.destination_city = destination_city
        self.date_from = date_from
        self.date_to = date_to
        self.interests = interests

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()

        city_info_agent = agents.city_info_agent()
        logistics_expert_agent = agents.logistics_expert_agent()
        itinerary_planner_agent = agents.itinerary_planner_agent()
        language_guide_agent = agents.language_guide_agent()

        city_info = tasks.city_info_task(
            city_info_agent, self.from_city, self.destination_city, 
            self.interests, self.date_from, self.date_to
        )

        plan_logistics = tasks.plan_logistics_task(
            [city_info], logistics_expert_agent,
            self.destination_city, self.interests, self.date_from, self.date_to
        )

        build_itinerary = tasks.build_itinerary_task(
            [city_info, plan_logistics],
            itinerary_planner_agent, self.destination_city,
            self.interests, self.date_from, self.date_to
        )

        language_guide = tasks.language_guide_task(
            [build_itinerary], language_guide_agent, self.destination_city
        )

        crew = Crew(
            agents=[city_info_agent, logistics_expert_agent, itinerary_planner_agent, language_guide_agent],
            tasks=[city_info, plan_logistics, build_itinerary, language_guide],
            process=Process.sequential,
            full_output=True,
            verbose=True
        )
        return crew.kickoff()

def load_markdown(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content.replace("```markdown", "").replace("```", "")
    except Exception as e:
        print(f"Erro ao carregar arquivo: {str(e)}")
        return None

########################## Função de conversão Markdown para pdf atualizado

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch
from reportlab.lib import colors



def convert_md_to_pdf(file_md, file_pdf):
    """
    Converte arquivo Markdown em PDF com detecção de títulos e listas.
    100% compatível com Streamlit Cloud.
    """
    text = load_markdown(file_md)
    if not text:
        return

    # Converte Markdown para HTML estruturado
    html_text = markdown2.markdown(text)

    # Quebra o HTML básico em blocos (parágrafos e listas)
    html_lines = html_text.split("\n")

    # Documento PDF
    doc = SimpleDocTemplate(
        file_pdf,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    normal.fontName = "Helvetica"
    normal.fontSize = 11
    normal.leading = 14

    h1 = ParagraphStyle("Heading1", parent=normal, fontSize=16, leading=18,
                        spaceAfter=8, textColor=colors.HexColor("#1a73e8"))
    h2 = ParagraphStyle("Heading2", parent=normal, fontSize=13, leading=16,
                        spaceAfter=6, textColor=colors.darkblue)

    story = []

    for line in html_lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 6))
            continue

        # Detecta headers convertidos pelo markdown2
        if line.startswith("<h1>"):
            content = re.sub(r"</?h1>", "", line)
            story.append(Paragraph(content, h1))
        elif line.startswith("<h2>"):
            content = re.sub(r"</?h2>", "", line)
            story.append(Paragraph(content, h2))
        elif line.startswith("<ul>"):
            # lista simples
            items = re.findall(r"<li>(.*?)</li>", line)
            if items:
                lista = ListFlowable(
                    [ListItem(Paragraph(item, normal)) for item in items],
                    bulletType='bullet',
                    leftIndent=15
                )
                story.append(lista)
        elif line.startswith("<p>"):
            content = re.sub(r"</?p>", "", line)
            story.append(Paragraph(content, normal))
        else:
            # fallback: texto simples
            story.append(Paragraph(re.sub(r"<.*?>", "", line), normal))

        story.append(Spacer(1, 4))

    doc.build(story)



##################################################################
def clear_output():
    for item in os.listdir(OUTPUT_DIR):
        os.remove(os.path.join(OUTPUT_DIR, item))
    st.success("🧹 Conteúdo removido com sucesso!")
    st.rerun()

# ==========================================================
# FORMULÁRIO DE VIAGEM
# ==========================================================

with st.form("trip_form"):
    st.subheader("✈️ Informe os detalhes da sua viagem")

    from_city = st.text_input("Cidade de origem:")
    destination_city = st.text_input("Cidade de destino:")

    col1, col2 = st.columns(2)
    with col1:
        date_from = st.date_input("Data de partida:")
    with col2:
        date_to = st.date_input("Data de retorno:")

    interests = st.text_area("Interesses e preferências:")

    col_submit, col_clear = st.columns(2)
    with col_submit:
        submitted = st.form_submit_button("🚀 Gerar roteiro")
    with col_clear:
        clear_pressed = st.form_submit_button("🧹 Limpar conteúdo")

if clear_pressed:
    clear_output()

if submitted:
    if not (from_city and destination_city and interests):
        st.warning("Por favor, preencha todos os campos do formulário")
    else:
        with st.status("Montando seu roteiro... Isso pode levar alguns instantes..."):
            trip_crew = TripCrew(from_city, destination_city, date_from, date_to, interests)
            result = trip_crew.run()

        for md_file, pdf_file in files.items():
            convert_md_to_pdf(md_file, os.path.join(OUTPUT_DIR, pdf_file))
            if os.path.exists(md_file):
                shutil.move(md_file, os.path.join(OUTPUT_DIR, md_file))
        st.success("✅ Roteiro gerado com sucesso!")

files_md = [md for md in files if os.path.exists(os.path.join(OUTPUT_DIR, md))]
if len(files_md) == len(files):
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Roteiro de Viagem",
        "📖 Guia de Comunicação",
        "📍 Relatório Cidade",
        "✈️ Relatório Logística"
    ])
    with tab1: st.markdown(load_markdown(os.path.join(OUTPUT_DIR, "roteiro_viagem.md")))
    with tab2: st.markdown(load_markdown(os.path.join(OUTPUT_DIR, "guia_comunicacao.md")))
    with tab3: st.markdown(load_markdown(os.path.join(OUTPUT_DIR, "relatorio_local.md")))
    with tab4: st.markdown(load_markdown(os.path.join(OUTPUT_DIR, "relatorio_logistica.md")))

    st.divider()
    st.subheader("📥 Downloads")

    for md_file, pdf_file in files.items():
        pdf_path = os.path.join(OUTPUT_DIR, pdf_file)
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label=f"📄 Baixar {pdf_file}",
                    data=f,
                    file_name=pdf_file,
                    mime="application/pdf"
                )

    zip_path = os.path.join(OUTPUT_DIR, "pacote_viagem.zip")
    shutil.make_archive(zip_path.replace(".zip", ""), 'zip', OUTPUT_DIR)
    with open(zip_path, "rb") as f:
        st.download_button(
            label="📦 Baixar todos os arquivos (ZIP)",
            data=f,
            file_name="planejamento_viagem_completo.zip",
            mime="application/zip"
        )

    st.divider()
    st.info("🤖 Desenvolvido por Vinicius Meireles | AgentAI Trip 2025")