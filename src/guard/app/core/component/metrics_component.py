import pandas as pd
from decouple import config
from prometheus_api_client import PrometheusConnect

from common_consts import PROMETHEUS_ENDPOINT

prom = PrometheusConnect(url=config(PROMETHEUS_ENDPOINT), disable_ssl=True)


def get_stats_for_24h(user: str, topic: str) -> pd.DataFrame:
    metric_data = prom.custom_query(
        "increase(" + topic + "{toxic_client_id='" + user + "'}[1h])[24h:1h]"
    )

    result = pd.DataFrame(columns=["timestamp", "value"])
    if len(metric_data) != 0:
        result = pd.DataFrame(metric_data[0]["values"], columns=["timestamp", "value"])
        result["timestamp"] = pd.to_datetime(result["timestamp"], unit='s').sort_values()
    result = result.reset_index(drop=True)
    return result


def get_toxic_stats_for_24h(user: str) -> pd.DataFrame:
    return get_stats_for_24h(user, "input_toxic_text_total")


def get_all_stats_for_24h(user: str) -> pd.DataFrame:
    return get_stats_for_24h(user, "input_text_total")


if __name__ == "__main__":
    name = "test"
    toxic = get_toxic_stats_for_24h(name)
    casual = get_all_stats_for_24h(name)
    casual = casual.rename(columns={"value": "Casual"})

    casual["Toxic"] = toxic["value"]
    print(casual)
