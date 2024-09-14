from time import sleep

import streamlit as st

from auth.jwt_handler import verify_access_token
from pages.api import filter_profile
from pages.common.cookies import cookie_manager


def make_sidebar():
    access_token = cookie_manager.get("access_token")
    with st.sidebar:
        if access_token and access_token != "":
            user_name, logout_button = st.columns([3, 1])
            with user_name:
                try:
                    user = verify_access_token(access_token)
                except Exception as e:
                    logout()

                if "user" in user:
                    user_name = user["user"]
                    if st.button(f"{user_name} profile", use_container_width=True):
                        st.switch_page("pages/profile.py")

            with logout_button:
                if st.button("Logout", type="primary"):
                    logout()

            if "messages" not in st.session_state:
                st.session_state.messages = []

            if prompt := st.chat_input("What is up?"):
                toxic_status = filter_profile.filter_validation(filter_type="general_filter", text=prompt)

                with st.chat_message("AI Filter"):
                    text = toxic_status["llm_answer"] if toxic_status["is_toxic"] else toxic_status["llm_answer"]
                    input_tags = ["#" + i["details"]["topic_detector"] for i in toxic_status["input_validation"] if
                                  "topic_detector" in i["details"]]
                    output_tags = ["#" + i["details"]["topic_detector"] for i in toxic_status["answer_validation"] if
                                   "topic_detector" in i["details"]]

                    if len(output_tags) != 0:
                        text = text + "\n\n [[Возможные темы ответа: " + ', '.join(output_tags) + ']]'

                    if len(input_tags) != 0:
                        text = text + "\n\n [[Возможные темы вопроса: " + ', '.join(input_tags) + ']]'

                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.messages.append({"role": "AI", "content": text})

            for message in st.session_state.messages[::-1]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])


def logout():
    cookie_manager.set("access_token", "")
    sleep(0.5)
    st.switch_page("home.py")
