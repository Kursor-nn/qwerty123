import json

import httpx
from decouple import config

from common_consts import GRAFANA_ENDPOINT, GRAFANA_SERVICE_TOKEN, GRAFANA_FOLDER_UID
from core.templates.alarm_rules_templates import build_alarm_rule_request

grafana_endpoint = config(GRAFANA_ENDPOINT)
grafana_service_token = config(GRAFANA_SERVICE_TOKEN)
grafana_folder_uid = config(GRAFANA_FOLDER_UID)

GRAFANA_CREATE_ALARM_RULE_ENDPOINT = f"{grafana_endpoint}/api/v1/provisioning/alert-rules"
GRAFANA_GET_ALARM_RULE_ENDPOINT = f"{grafana_endpoint}/api/v1/provisioning/alert-rules/"

grafana_service_account_headers = {
    "Authorization": f"Bearer {grafana_service_token}",
    "accept": "application/json",
    "Content-Type": "application/json"
}


def delete_alarm_rule(rule_id: str):
    response = httpx.delete(
        url=f"{grafana_endpoint}/api/v1/provisioning/alert-rules/{rule_id}",
        headers=grafana_service_account_headers)

    return response.status_code in (204, 500), "Rule is removed"


def create_alarm_rule(rule_id: str, rule_title: str, notification_topic: str, client_id: str):
    request = build_alarm_rule_request(rule_id, rule_title, grafana_folder_uid, client_id, notification_topic)
    response = httpx.post(
        url=GRAFANA_CREATE_ALARM_RULE_ENDPOINT,
        json=json.loads(request), headers=grafana_service_account_headers)

    payload = response.json()
    if "message" in payload:
        return True, payload["message"], rule_id
    return True, "Contact is created", rule_id


def get_alarm_rule_by_id(alarm_rule_id: str):
    response = httpx.get(
        url=GRAFANA_GET_ALARM_RULE_ENDPOINT + str(alarm_rule_id),
        headers=grafana_service_account_headers)
    return response.json()
