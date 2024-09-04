import pandas as pd
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

st.text(f"Home page configuration")
all_message = st.checkbox("All message statistic")
toxic_message = st.checkbox("Toxic statistic")
notification_stats = st.checkbox("Notification statistic")
stats_per_user = st.checkbox("Statistic per user")

st.text(f"Filters List")

toxic_filter = st.checkbox("Toxic Filter")
topic_filter = st.checkbox("Topic Filter")
prompt_filter = st.checkbox("Prompt Filter")

st.text(f"Notifications")
df = pd.DataFrame(
    [
        {"service": "telegrams", "receiver": "adasasdasdas", "is_widget": True},
        {"service": "emails", "receiver": "test@test.com", "is_widget": False}
    ]
)
edited_df = st.data_editor(df)
