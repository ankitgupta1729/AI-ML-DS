import streamlit as st
from query import query

st.set_page_config(page_title="Chatbot App", page_icon="🤖")
st.title("🤖 Chatbot App")
st.caption("Ask me about Red30 Shoes — returns, shipping, products, and more.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

_role_for = {"human": "user", "ai": "assistant"}

for msg in st.session_state.chat_history:
    with st.chat_message(_role_for.get(msg.type, "user")):
        st.markdown(msg.content)

if prompt := st.chat_input("Ask a question..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query(prompt, chat_history=st.session_state.chat_history)
        st.markdown(response["answer"])
