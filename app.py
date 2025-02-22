import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/chat"

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False  # Track if bot is thinking
if "user_message" not in st.session_state:
    st.session_state.user_message = ""  # Store user input before clearing it

st.set_page_config(page_title="FAQ Chatbot", layout="wide")

st.title("💬 FAQ Chatbot")
st.markdown("Ask me anything and I'll respond instantly!")

# Chat display container
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message("user" if msg["role"] == "You" else "assistant"):
            st.markdown(msg["content"])

# User input and send button
with st.container():
    user_input = st.text_input(
        "Type your message...", 
        key="user_input", 
        help="Press Enter or click Send", 
        value=st.session_state.user_message,  # Preserve value
        on_change=lambda: st.session_state.update({"send_triggered": True})  # Track enter key press
    )
    send_btn = st.button("Send", use_container_width=True, disabled=st.session_state.processing)

# Handle message sending
if (send_btn or st.session_state.get("send_triggered", False)) and user_input.strip() and not st.session_state.processing:
    st.session_state.processing = True  # Disable button while thinking
    st.session_state.send_triggered = False  # Reset Enter key trigger
    st.session_state.user_message = user_input  # Save input before clearing
    st.rerun()

if st.session_state.processing:
    with st.chat_message("user"):
        st.markdown(st.session_state.user_message)

    st.session_state.messages.append({"role": "You", "content": st.session_state.user_message})

    with st.spinner("Thinking..."):
        response = requests.post(API_URL, json={"query": st.session_state.user_message}).json()
        bot_response = response.get('response', 'I am not sure how to respond.').split("Final Answer:")[-1].strip()

    with st.chat_message("assistant"):
        st.markdown(bot_response)

    st.session_state.messages.append({"role": "Bot", "content": bot_response})

    # Reset processing state and clear input field
    st.session_state.processing = False
    st.session_state.user_message = "" 
    
    st.rerun()