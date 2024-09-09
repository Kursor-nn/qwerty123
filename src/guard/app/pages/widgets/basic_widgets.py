import numpy as np
import pandas as pd
import streamlit as st

from core.component.metrics_component import get_all_stats_for_24h, get_toxic_stats_for_24h


def display_24_hours(user: str, label: str):
    toxic = get_toxic_stats_for_24h(user)
    casual = get_all_stats_for_24h(user)

    casual = casual.rename(columns={"value": "Casual"})
    casual["Toxic"] = toxic["value"]
    casual = casual.reset_index()

    st.text(label)
    st.bar_chart(casual[["Casual", "Toxic"]], height=500, color=["#0000FF", "#FF0000"])


def display_toxic_24_hours(user: str, label: str):
    toxic = get_toxic_stats_for_24h(user)
    toxic = toxic.reset_index()
    st.text(label)
    st.bar_chart(toxic["value"], color=["#FF0000"], height=500)


def display_notifications_stats(user: str, label: str):
    st.text(label)
    df = pd.DataFrame(
        {
            "Notification Service": ["Telegram", "Emails"],
            "Status": ["Enabled", "Disabled"],
            "Today": [np.random.randint(0, 1000) for _ in range(2)],
            "Toxic today": [np.random.randint(0, 1000) for _ in range(2)],
            "Threshold per hours": [np.random.randint(0, 1000) for _ in range(2)],
            "Notification History": [[np.random.randint(0, 5000) for _ in range(30)] for _ in range(2)],
        }
    )
    st.dataframe(
        df,
        column_config={
            "name": "App name",
            "stars": st.column_config.NumberColumn(
                "Github Stars",
                help="Number of stars on GitHub",
                format="%d ⭐",
            ),
            "Notification History": st.column_config.LineChartColumn(
                "Views (past 30 days)", y_min=0, y_max=5000
            ),
        },
        hide_index=True,
    )


def display_toxic_clients(user: str, label: str):
    st.text(user)

    df = pd.DataFrame(
        [
            {"client id": "1", "toxic": 1, "normal": 100, "recommendation": "to disable",
             "toxic history": [np.random.randint(0, 5000) for _ in range(30)]},
            {"client id": "2", "toxic": 12, "normal": 1000, "recommendation": "n/a",
             "toxic history": [np.random.randint(0, 5000) for _ in range(30)]},
        ]
    )
    st.data_editor(df, column_config={
        "toxic history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    })
