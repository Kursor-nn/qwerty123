import numpy as np
import pandas as pd
import streamlit as st


def display_24_hours(name):
    casual = np.random.randint(0, 101, size=24)
    toxic = np.random.randint(-101, 1, size=24)

    data = pd.DataFrame(np.vstack((casual, toxic)).T, columns=["Toxic", "Casual"])
    st.text(name)
    st.bar_chart(data, color=["#FF0000", "#0000FF"])


def display_toxic_24_hours(name):
    toxic = np.random.randint(-101, 1, size=24)
    chart_data = pd.DataFrame(np.abs(toxic), columns=["Toxic"])
    st.text(name)
    st.bar_chart(chart_data, color=["#FF0000"])


def display_notifications_stats(name):
    st.text(name)
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


def display_toxic_clients(name):
    st.text(name)

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
