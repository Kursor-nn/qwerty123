from time import sleep

import streamlit as st

from core.cookies.cookies import cookie_manager


def make_sidebar():
    access_token = cookie_manager.get("access_token")
    print("access_token", access_token)
    with st.sidebar:
        st.title("Йцукен123")
        st.write("")

        if access_token or access_token != "":
            if st.button("Logout", type="primary"):
                logout()


def logout():
    cookie_manager.set("access_token", "")
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("home.py")
