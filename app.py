import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/chat"

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Apply modern styling
st.markdown(
    """
    <style>
    .message-container {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        width: fit-content;
        max-width: 80%;
    }
    .user-message {
        background-color: #0078FF;
        color: white;
        align-self: flex-end;
    }
    .bot-message {
        background-color: #F1F1F1;
        color: black;
        align-self: flex-start;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💬 FAQ Chatbot")
st.markdown("Ask me anything and I'll respond instantly!")

# Chat display using markdown
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        role = "👤 You" if msg["role"] == "You" else "🤖 Bot"
        style_class = "user-message" if msg["role"] == "You" else "bot-message"
        st.markdown(
            f'<div class="message-container {style_class}"><strong>{role}:</strong> {msg["content"]}</div>',
            unsafe_allow_html=True,
        )

# User input field
user_input = st.text_input("Type your message...", key="user_input", help="Press Enter or click Send")

# Send button
if st.button("Send", use_container_width=True):
    if user_input.strip():
        st.session_state.messages.append({"role": "You", "content": user_input})
        
        response = requests.post(API_URL, json={"query": user_input}).json()
        bot_response = response['response'].split("Final Answer:")[-1].strip()
        
        st.session_state.messages.append({"role": "Bot", "content": bot_response})
        st.rerun()
    else:
        st.warning("Please enter a message!")

# Ensure smooth layout updates
st.markdown("<script>window.scrollTo(0,document.body.scrollHeight);</script>", unsafe_allow_html=True)
