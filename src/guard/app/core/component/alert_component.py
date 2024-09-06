import json

import httpx
from decouple import config

from common_consts import GRAFANA_ENDPOINT, GRAFANA_SERVICE_TOKEN, GRAFANA_FOLDER_UID
from core.component.alarm_rules_templates import alert_template

grafana_endpoint = config(GRAFANA_ENDPOINT)
grafana_service_token = config(GRAFANA_SERVICE_TOKEN)
grafana_folder_uid = config(GRAFANA_FOLDER_UID)

grafana_service_account_headers = {
    "Authorization": "Bearer {grafana_service_token}",
    "accept": "application/json",
    "Content-Type": "application/json"
}


def delete_alarm_rule(rule_id: str):
    response = httpx.delete(
        url=f"{grafana_endpoint}/api/v1/provisioning/alert-rules/{rule_id}",
        headers=grafana_service_account_headers)

    return response.status_code in (204, 500), "Rule is removed"


def create_alarm_rule(rule_id: str, rule_title: str, notification_topic: str, client_id: str):
    request = alert_template.replace("{USER-ALERT-RULE-ID}", rule_id).replace("{USER-ALERT-TITLE-ID}", rule_title).replace(
        "{USER-NOTIFICATION-ID}", notification_topic).replace("{CLIENT_ID}", client_id).replace("{FOLDER_UID}", grafana_folder_uid)

    response = httpx.post(
        url="{grafana_endpoint}/api/v1/provisioning/alert-rules",
        json=json.loads(request), headers=grafana_service_account_headers)

    payload = response.json()
    if "message" in payload:
        return True, payload["message"], rule_id
    return True, "Contact is created", rule_id


def get_alarm_rule_by_id(alarm_rule_id: str):
    response = httpx.get(
        url=f"{grafana_endpoint}/api/v1/provisioning/alert-rules/{alarm_rule_id}",
        headers=grafana_service_account_headers)
    return response.json()


def toggle_alarm_rule(alarm_rule_id: str, status: bool):
    current_state = get_alarm_rule_by_id(alarm_rule_id)
    current_state["isPaused"] = status

    response = httpx.put(
        url=f"{grafana_endpoint}/api/v1/provisioning/alert-rules/{alarm_rule_id}",
        json=current_state, headers=grafana_service_account_headers)

    payload = response.json()
    if "message" in payload:
        return True, payload["message"]
    return True, "Contact is created"
