import streamlit as st

from pages.api.user_profile import password_entered, create_user
from pages.common.cookies import get_cookie_manager


def display_start_page():
    login_tab, registration_tab = st.tabs(["Login", "Register"])

    with login_tab:
        username = st.text_input("Login", key="username")
        password = st.text_input("Password", type="password", key="password")

        if st.button("Sign in", type="primary", key="signin"):
            result = password_entered(username, password)
            if result.status_code in [401, 404]:
                error_desc = result.json()["detail"]
                st.write(f"{error_desc}")
            else:
                val = result.json()["access_token"]
                get_cookie_manager().set("access_token", val)
                st.success("Logged in successfully!")

                st.switch_page("home.py")

    with registration_tab:
        st.write(f"Register a new user.")

        login = st.text_input("Login")
        user_password = st.text_input("Password")
        email_address = st.text_input("Email")

        if st.button("Sign up", type="primary", key="sign_up"):
            result = create_user(login, user_password, email_address)

            if result.status_code == 200:
                message = result.json()
                st.write(message["message"])
                st.switch_page("home.py")
            else:
                message = result.json()
                st.write(message)
