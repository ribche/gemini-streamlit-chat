import os
import streamlit as st
import google.generativeai as genai

#load streamlit secrets key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Smartchef App", layout="centered")
st.title("GeminiChat-StreamlitUI")

#initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

#write out previous messages
for msg in st.session_state.messages:
    role, content = msg["role"], msg["content"]
    if role == "user":
        st.markdown(f"** You:** {content}")
    else:
        st.markdown(f"** Gemini:** {content}")

#input window
user_input = st.text_input("Write your message:", "")

#if user clicks enter
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = model.generate_content(user_input)       #send to gemini
    reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.experimental_rerun()
    