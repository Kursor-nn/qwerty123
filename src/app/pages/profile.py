import streamlit as st

from core.cookies.cookies import get_cookie_manager
from pages.api.user_profile import get_profile_info, toggle_feature
from pages.common.navigation import make_sidebar

make_sidebar()

st.title("Profile")

access_token = get_cookie_manager().get("access_token")

if not access_token:
    st.switch_page("home.py")

profile_info = get_profile_info()

filters = [i for i in profile_info.features if i.type == "filter"]
notifications = [i for i in profile_info.features if i.type == "notification"]
stats = [i for i in profile_info.features if i.type == "statis"]


def change_value_for_stats(toggle_feature_id: str, value: bool):
    def inner():
        x = toggle_feature_id
        y = value
        toggle_feature(x, y)

    return inner


def build_check_box_for(label, values):
    st.text(label)

    for item in values:
        st.checkbox(item.name, value=item.enabled, key=f"{item.name}-{item.feature_type_id}",
                    on_change=change_value_for_stats(item.feature_type_id, not item.enabled))


build_check_box_for("Home page configuration", stats)
build_check_box_for("Filters List", filters)
build_check_box_for("Notifications", notifications)
