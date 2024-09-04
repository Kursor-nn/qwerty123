import streamlit as st

from core.auth.jwt_handler import verify_access_token
from core.cookies.cookies import get_cookie_manager
from pages.common.navigation import make_sidebar

make_sidebar()

st.title("Profile")

access_token = get_cookie_manager().get("access_token")

if not access_token:
    st.switch_page("home.py")

login = verify_access_token(access_token)["user"]
header = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

st.text(f"User ID: {login}")

