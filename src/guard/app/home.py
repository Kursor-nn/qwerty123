import streamlit as st

from core.cookies.cookies import get_cookie_manager
from pages.api.user_profile import get_profile_info
from pages.common.navigation import make_sidebar
from pages.widgets.basic_widgets import display_24_hours, display_notifications_stats, display_toxic_clients
from pages.widgets.reg_sign_widgets import display_start_page

make_sidebar()

access_token = get_cookie_manager().get("access_token")


def display_widget(widget_name, widget_function):
    feature = [i for i in profiles.features if i.name == widget_name]
    if len(feature) != 0 and feature[0].enabled:
        widget_function()


st.title("Welcome!")

if not access_token or access_token == "":
    display_start_page()
else:
    profiles = get_profile_info()

    display_widget("24 hour dynamic", lambda: display_24_hours("24 hour dynamic"))
    display_widget("Toxic messages 24 hour dynamic", lambda: display_24_hours("Toxic messages 24 hour dynamic"))
    display_widget("Notifications Stats", lambda: display_notifications_stats("Notifications Stats"))
    display_widget("Toxic clients", lambda: display_toxic_clients("Toxic clients"))