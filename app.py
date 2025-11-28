import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# ---------- CONFIG: API KEY & MODEL ----------

# preberi .env (lokalno) + environment spremenljivke (Railway)
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash-lite"  # model, ki ti je delal v test.py

if not API_KEY:
    st.set_page_config(page_title="GeminiChat-StreamlitUI", layout="centered")
    st.error(
        "❌ GEMINI_API_KEY ni nastavljen.\n\n"
        "Lokalno dodaj .env datoteko z vrstico:\n"
        'GEMINI_API_KEY="tvoj_kljuc"\n\n'
        "Na Railwayu pa v Variables nastavi isto ime spremenljivke."
    )
    st.stop()

# konfiguriraj Gemini SDK
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# ---------- STREAMLIT UI ----------

st.set_page_config(page_title="GeminiChat-StreamlitUI", layout="centered")
st.title("GeminiChat-StreamlitUI")

st.write("Write your message:")

# inicializiraj zgodovino sporočil
if "messages" not in st.session_state:
    st.session_state.messages = []  # vsako sporočilo: {"role": "user"/"assistant", "content": "..."}

# izpiši zgodovino v obliki chat mehurčkov
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# vnosno polje spodaj
user_input = st.chat_input("Napiši sporočilo...")

if user_input:
    # dodaj user msg v zgodovino
    st.session_state.messages.append({"role": "user", "content": user_input})

    # prikaz uporabnikovega sporočila
    with st.chat_message("user"):
        st.markdown(user_input)

    # klic na Gemini
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_Thinking..._")

        try:
            # za enostavnost damo modelu samo zadnje sporočilo
            response = model.generate_content(user_input)
            reply_text = response.text
        except Exception as e:
            reply_text = f"❌ Error calling Gemini API:\n\n`{e}`"

        placeholder.markdown(reply_text)

    # shrani odgovor v zgodovino
    st.session_state.messages.append({"role": "assistant", "content": reply_text})
