import streamlit as st

st.title("Assistente Banco Ágil")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("What is up?")
if prompt:
    prompt = f"Eu: {prompt}"

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Assistente: {prompt}"

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
