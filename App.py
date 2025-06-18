import streamlit as st
import openai
import os

# ✅ Set your OpenRouter API key here
openai.api_key = "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"  # replace with your key
openai.api_base = "https://openrouter.ai/api/v1"

st.set_page_config(page_title="🤖 Nova Bot ")

st.title("🤖 Nova ChatBot")

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(msg["user"])
    with st.chat_message("assistant"):
        st.markdown(msg["bot"])

user_input = st.chat_input("Say something...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    reply = response["choices"][0]["message"]["content"]
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.history.append({"user": user_input, "bot": reply})
