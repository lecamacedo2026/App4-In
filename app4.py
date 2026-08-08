import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


# Configuração da página Streamlit
st.set_page_config(page_title="Assistente IA", page_icon="✈️", layout="centered")
st.title("Painel de Comunicação")

# Recupera a chave da API do ambiente seguro
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Erro de Configuração: A chave GROQ_API_KEY não foi encontrada nas variáveis de ambiente.")
    st.stop()

# Inicialização do cliente Groq
client = Groq(api_key=api_key)

# Interface de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        )
        response = completion.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Falha na comunicação com o servidor Groq: {e}")