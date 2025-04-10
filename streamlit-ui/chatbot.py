import requests
import streamlit as st
import os

OLLAMA_URL = f"http://{os.getenv('OLLAMA_HOST')}:{os.getenv('OLLAMA_PORT')}"
MODEL_NAME = os.getenv("OLLAMA_MODEL")

# Fungsi untuk mengirim prompt ke Ollama
def ask_ollama(prompt):
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response from model.")
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

# UI Streamlit
st.set_page_config(page_title="Local Chatbot")
st.title("Chat with Ollama Model")
st.caption(f"Model in use:   :green-badge[ {MODEL_NAME} ]")

# Inisialisasi sesi chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input user
user_input = st.chat_input("Ask me anything...")

# Proses pertanyaan
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Thinking..."):
        bot_response = ask_ollama(user_input)
    st.session_state.chat_history.append(("assistant", bot_response))

# Tampilkan riwayat chat
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)