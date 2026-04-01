import streamlit as st
import requests

st.set_page_config(page_title="Multi-Agent UI", page_icon="🤖")
st.title("🤖 AI Agent Assistant")

API_URL = "http://localhost:8000/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("How can I help with your tasks?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Send request to FastAPI
        payload = {"message": prompt, "thread_id": "user_1"}
        
        with requests.post(API_URL, json=payload, stream=True) as r:
            for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
        
        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
import subprocess
import sys

def run_streamlit():
    # This runs the streamlit command as a background process
    subprocess.run([sys.executable, "-m", "streamlit", "run", "mf_ai_agent/frontend.py"])

if __name__ == "__main__":
    run_streamlit()