import streamlit as st
from main import AgentController

title = "Atendimento - Banco Ágil"
description = "Seja bem-vindo(a) ao atendimento do Banco Ágil!"

st.set_page_config(page_title=title, page_icon="🤖")

st.title(title)
st.text(description)

if "controller" not in st.session_state:
    st.session_state.controller = AgentController()

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

for m in st.session_state.conversation_history:
    if m["role"] != 'system':
        with st.chat_message(m["role"]):
            st.write(m["content"])

user_input = st.chat_input("Digite sua mensagem...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.conversation_history = st.session_state.controller.send(user_input, st.session_state.conversation_history)
    agent_response = st.session_state.conversation_history[-1]["content"]

    with st.chat_message("assistant"):
        st.write(agent_response)
