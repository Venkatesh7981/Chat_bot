import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Buddy Bot!",
    page_icon=":brain:",
    layout="centered",
)

# Retrieve API key from environment variables or directly paste (NOT RECOMMENDED)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Fallback to hardcoded API key (REMOVE THIS IN PRODUCTION)
if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# Check if API key is available
if not GOOGLE_API_KEY:
    st.error("❗API key not found. Please check your environment variables.")
    st.stop()

# Set up Google Gemini AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Select the correct model
model_name = "models/gemini-1.5-pro-latest"  # Updated to correct model
model = gen_ai.GenerativeModel(model_name)

# Function to translate roles between Gemini and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chatbot title
st.title("🤖 Buddy ChatBot")

# Apply custom CSS for chat styling
st.markdown(
    """
    <style>
        /* Set background color for the entire page */
        body {
            background-color: #f5f7fa;
        }
        /* Set background for the Streamlit main content */
        .main {
            background-color: #f5f7fa;
            padding: 20px;
            border-radius: 10px;
        }
        .chat-box {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .user-message {
            color: #333333;
            background-color: #ffffff;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
            display: inline-block;
            border: 1px solid #ddd;
        }
        .assistant-message {
            color: #333333;
            background-color: #ffffff;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
            display: inline-block;
            border: 1px solid #ddd;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Display chat history
for message in st.session_state.chat_session.history:
    role = translate_role_for_streamlit(message.role)
    with st.chat_message(role):
        st.markdown(
            f'<div class="{"assistant-message" if role == "assistant" else "user-message"}">{message.parts[0].text}</div>',
            unsafe_allow_html=True,
        )

# Input field for user message
user_prompt = st.chat_input("Ask Buddy chatbot...")
if user_prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(f'<div class="user-message">{user_prompt}</div>', unsafe_allow_html=True)

    try:
        # Send message to Gemini-Pro and receive response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Check if response is valid
        if gemini_response and hasattr(gemini_response, "text"):
            # Display assistant's response
            with st.chat_message("assistant"):
                st.markdown(
                    f'<div class="chat-box">{gemini_response.text}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.error("❗ No response received. Please try again.")
    except Exception as e:
        st.error(f"❗ An error occurred: {str(e)}")
