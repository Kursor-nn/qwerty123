from time import sleep

import streamlit as st

from core.cookies.cookies import cookie_manager
from pages.api import filter_profile


def make_sidebar():
    access_token = cookie_manager.get("access_token")
    with st.sidebar:
        st.title("Йцукен123")

        if access_token or access_token != "":
            if st.button("Logout", type="primary"):
                logout()

            if "messages" not in st.session_state:
                st.session_state.messages = []

            if prompt := st.chat_input("What is up?"):
                toxic_status = filter_profile.filter_validation(prompt)

                with st.chat_message("AI Filter"):
                    text = toxic_status["llm_answer"] if toxic_status["is_toxic"] else toxic_status["llm_answer"]
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.messages.append({"role": "AI", "content": text})

            for message in st.session_state.messages[::-1]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])


def logout():
    cookie_manager.set("access_token", "")
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("home.py")
