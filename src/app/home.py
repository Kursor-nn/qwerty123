import httpx
import numpy as np
import pandas as pd
import streamlit as st
from decouple import config

from core.cookies.cookies import get_cookie_manager
from pages.common.navigation import make_sidebar
from utils.const import BACKEND_HOST

make_sidebar()

access_token = get_cookie_manager().get("access_token")

def password_entered():
    data = {
        "login": username,
        "password": password
    }
    headers = {'Content-type': 'application/json'}
    res = httpx.post(url=f"{config(BACKEND_HOST)}/api/user/signin", json=data, headers=headers)
    return res


def create_user():
    data = {
        "login": login,
        "password": user_password,
        "email": email_address,
    }

    headers = {'Content-type': 'application/json'}
    res = httpx.post(url=f"{config(BACKEND_HOST)}/api/user/register", json=data, headers=headers)
    return res


st.title("Welcome!")

if not access_token or access_token == "":
    loginTab, registrationTab = st.tabs(["Login", "Register"])

    with loginTab:
        username = st.text_input("Login", key="username")
        password = st.text_input("Password", type="password", key="password")

        if st.button("Sign in", type="primary", key="signin"):
            result = password_entered()
            if result.status_code in [401, 404]:
                error_desc = result.json()["detail"]
                st.write(f"{error_desc}")
            else:
                val = result.json()["access_token"]
                get_cookie_manager().set("access_token", val)
                st.success("Logged in successfully!")

                st.switch_page("home.py")

    with registrationTab:
        st.write(f"Register a new user.")

        login = st.text_input("Login")
        user_password = st.text_input("Password")
        email_address = st.text_input("Email")

        if st.button("Sign up", type="primary", key="sign_up"):
            result = create_user()

            if result.status_code == 200:
                message = result.json()
                st.write(message["message"])
                st.switch_page("home.py")
            else:
                message = result.json()
                st.write(message)
else :
    casual = np.random.randint(0, 101, size=24)
    toxic = np.random.randint(-101, 1, size=24)

    chart_data = pd.DataFrame(np.vstack((casual, toxic)).T, columns=["Toxic", "Casual"])
    st.text("24 hour dynamic")
    st.bar_chart(chart_data, color=["#FF0000", "#0000FF"])

    chart_data = pd.DataFrame(np.abs(toxic), columns=["Toxic"])
    st.text("Toxic messages 24 hour dynamic")
    st.bar_chart(chart_data, color=["#FF0000"])



