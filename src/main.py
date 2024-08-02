import os
import json
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Boney Chat",
    page_icon="🐐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #121212; /* Dark background color */
    }
    .stApp {
        color: #e0e0e0; /* Light text color for readability */
        font-family: 'Arial', sans-serif;
    }
    .stTitle {
        color: #bb86fc; /* Light purple color for title */
    }
    .chat-message.user {
        background-color: #333333; /* Darker gray for user messages */
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #444; /* Slightly lighter gray border */
    }
    .chat-message.assistant {
        background-color: #424242; /* Dark gray for assistant messages */
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #555; /* Slightly lighter gray border */
    }
    .stChatInput input {
        border-radius: 20px;
        border: 1px solid #bb86fc; /* Light purple border for input */
        padding: 10px;
        font-size: 16px;
        background-color: #333; /* Dark background for input */
        color: #e0e0e0; /* Light text color for input */
    }
    .stButton {
        background-color: #bb86fc; /* Light purple color for buttons */
        color: #121212; /* Dark text color for buttons */
        border-radius: 5px;
    }
    .stButton:hover {
        background-color: #9a67ea; /* Darker purple on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(working_dir, 'config.json')

try:
    with open(config_path, 'r') as f:
        config_content = f.read().strip()
        if not config_content:
            raise ValueError("config.json is empty")
        config_data = json.loads(config_content)
    GROQ_API_KEY = config_data.get("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in config.json")
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY
except FileNotFoundError:
    st.error("Configuration file not found.")
    st.stop()
except json.JSONDecodeError as e:
    st.error(f"Error reading config.json: {e.msg}")
    st.stop()
except ValueError as e:
    st.error(str(e))
    st.stop()

client = Groq()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🐐 Boney Chat")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

user_prompt = st.chat_input("Ask the bot...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt, unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": "hello"},
        *st.session_state.chat_history
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        assistant_response = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

        with st.chat_message("assistant"):
            st.markdown(assistant_response, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")
