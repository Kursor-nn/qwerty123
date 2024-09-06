import json

import httpx

from core.component.alarm_rules_templates import alert_template


def delete_alarm_rule(rule_id: str):
    response = httpx.delete(
        url=f"http://grafana:3000/api/v1/provisioning/alert-rules/{rule_id}",
        headers={
            "Authorization": "Bearer glsa_O30TNpVq9uXOZuS7gNw2u0VwEzYLRoot_cb8ae01e",
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    return response.status_code in (204, 500), "Rule is removed"


def create_alarm_rule(rule_id: str, rule_title: str, notification_topic: str, client_id: str):
    request = alert_template.replace("{USER-ALERT-RULE-ID}", rule_id).replace("{USER-ALERT-TITLE-ID}", rule_title).replace(
        "{USER-NOTIFICAITON-ID}", notification_topic).replace("{CLIENT_ID}", client_id)

    response = httpx.post(
        url="http://grafana:3000/api/v1/provisioning/alert-rules",
        json=json.loads(request), headers={
            "Authorization": "Bearer glsa_O30TNpVq9uXOZuS7gNw2u0VwEzYLRoot_cb8ae01e",
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    responst_data = response.json()
    if "message" in responst_data:
        print(responst_data)
        return True, response.json()["message"], rule_id
    return True, "Contact is created", rule_id


def get_alarm_rule_by_id(alarm_rule_id: str):
    response = httpx.get(
        url=f"http://grafana:3000/api/v1/provisioning/alert-rules/{alarm_rule_id}",
        headers={
            "Authorization": "Bearer glsa_O30TNpVq9uXOZuS7gNw2u0VwEzYLRoot_cb8ae01e",
            "accept": "application/json",
            "Content-Type": "application/json"
        })
    return response.json()


def toggle_alarm_rule(alarm_rule_id: str, status: bool):
    # request = {"isPaused": status}
    currentstate = get_alarm_rule_by_id(alarm_rule_id)
    currentstate["isPaused"] = status

    response = httpx.put(
        url=f"http://grafana:3000/api/v1/provisioning/alert-rules/{alarm_rule_id}",
        json=currentstate, headers={
            "Authorization": "Bearer glsa_O30TNpVq9uXOZuS7gNw2u0VwEzYLRoot_cb8ae01e",
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    responst_data = response.json()
    if "message" in responst_data:
        return True, response.json()["message"]
    return True, "Contact is created"


if __name__ == "__main__":
    print(create_alarm_rule(
        "alko-test-123",
        "alko-test-123-title",
        "test--1002200300374-notification",
        "test",
    ))
    # print(delete_alarm_rule("edx095oz0zbb4a"))
