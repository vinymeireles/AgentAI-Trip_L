import streamlit as st
import streamlit.components.v1 as components


# Style: CSS para esconder o menu hamburger (☰) e o footer
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
st.sidebar.image("Img/logoAI.png", width=200)

st.markdown("<h2 style='text-align: center; color: white;'>📞 Contatos</h2>", unsafe_allow_html=True)
st.markdown("")


st.markdown("Para desenvolvimento de novos projeto - Dashboard utilizando Inteligência Articial: Machine Learning e Agents AI.")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("Img/logo.png", width=250)


st.divider()
st.markdown("")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image("icons/whatsapp.png", caption="28 99918-3961", width=90)

with col2:
    st.image("icons/gmail.png", caption="viniciusmeireles@gmail.com", width=100)

with col3:
    st.image("icons/location.png", caption="Vitória/ES", width=90)    

with col4:
    st.image("icons/linkedin.png",caption= "/pviniciusmeireles", width=90)


