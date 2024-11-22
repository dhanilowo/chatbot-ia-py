import streamlit as st
from groq import Groq
from typing import Generator

st.set_page_config(page_title="Mi chat de IA", page_icon="🐻‍❄️", layout="centered")

st.title("Chatbot")
st.sidebar.title("Configuración de la IA")

client = Groq(
    api_key=st.secrets['groqAPIKeyTC'],
)

modelos=['llama3-8b-8192','llama3-70b-8192','mixtral-8x7b-32768']

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:   
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


if "messages" not in st.session_state:
    st.session_state.messages = []


with st.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

parModelo = st.sidebar.selectbox('Modelos',options=modelos,index=0)
prompt=st.chat_input("Ingresa tu consulta")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        chat_completion = client.chat.completions.create(
            model=parModelo,                       
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],
            stream=True
        )  
        with st.chat_message("assistant"):            
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)                                    
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(e)