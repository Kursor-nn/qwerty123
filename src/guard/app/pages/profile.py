import streamlit as st

from pages.api.user_profile import get_profile_info, toggle_feature, set_config
from pages.common.cookies import get_cookie_manager
from pages.common.navigation import make_sidebar

make_sidebar()

st.title("Profile")

access_token = get_cookie_manager().get("access_token")

if not access_token:
    st.switch_page("home.py")

profile_info = get_profile_info()

filters = [i for i in profile_info.features if i.type == "filter" or i.type == "filter_mode"]
notifications = [i for i in profile_info.features if i.type == "notification"]
stats = [i for i in profile_info.features if i.type == "statis"]
threshold = [i for i in profile_info.features if i.type == "threshold"]


def change_value_for_stats(toggle_feature_id: str, value: bool):
    def inner():
        fid = toggle_feature_id
        state = value
        toggle_feature(fid, state)

    return inner


def build_check_box_for(label, values):
    st.text(label)

    for item in values:
        st.checkbox(item.name, value=item.enabled, key=f"{item.name}-{item.feature_type_id}",
                    on_change=change_value_for_stats(item.feature_type_id, not item.enabled))


home_tab, filters_tab, notifications_tab, threshold_tab = st.tabs(["Home page configuration", "Filters List", "Notifications", "Threshold"])

with home_tab:
    build_check_box_for("Home page configuration", stats)

with filters_tab:
    input_columns, output_columns = st.columns(2)

    input_filters = [i for i in filters if "Request" in i.name]
    output_filters = [i for i in filters if "Answer" in i.name]

    another_filters = [i for i in filters if i.type == "filter_mode"]
    build_check_box_for("Filter Modes", another_filters)

    with input_columns:
        build_check_box_for("Input filters List", input_filters)

    with output_columns:
        build_check_box_for("Output filters List", output_filters)

with notifications_tab:
    build_check_box_for("Notifications", notifications)
    with st.popover("Add contact for notifications") as popup:
        option = st.selectbox(
            "How would you like to be contacted?",
            set([i.name for i in notifications]),
            index=None,
            placeholder="Select contact method...",
        )

        st.write("You selected:", option)
        address = st.text_input("Telegram chat name for notifications")
        nftid = [i.feature_type_id for i in notifications if i.name == option]

        st.button("Save", on_click=lambda: set_config(feature_type_id=nftid[0], value=address), use_container_width=True)

    for i in notifications:
        st.write(i.name, ":", i.config)

with threshold_tab:
    if len(threshold) > 0:
        ftid = threshold[0].feature_type_id
        threshold_state = st.checkbox(
            "Notification Threshold", value=threshold[0].enabled, key=f"{threshold[0].name}-{threshold[0].feature_type_id}",
            on_change=change_value_for_stats(threshold[0].feature_type_id, not threshold[0].enabled)
        )
        number = st.number_input("Toxic message threshold", min_value=10, max_value=5000, step=1)

        st.button("Push", on_click=lambda: set_config(feature_type_id=ftid, value=number), use_container_width=True)
