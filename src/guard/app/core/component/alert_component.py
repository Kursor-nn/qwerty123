import json

import httpx

from core.component.alarm_rules_templates import alert_template


def delete_alarm_rule(rule_id: str):
    response = httpx.delete(
        url=f"http://localhost:3000/api/v1/provisioning/alert-rules/{rule_id}",
        headers={
            "Authorization": "Bearer glsa_Dx4X1gQH0jQSS0I01Z9C6H4ppwm3Roj7_c4e1ab9a",
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    # responst_data = response.json()
    # if "message" in responst_data:
    # return True, response.json()["message"]
    return response.status_code in (204, 500), "Rule is removed"


def create_alarm_rule(rule_id: str, rule_title: str, notification_topic: str, client_id: str):
    request = alert_template.replace("{USER-ALERT-RULE-ID}", rule_id).replace("{USER-ALERT-TITLE-ID}", rule_title).replace("{USER-NOTIFICAITON-ID}", notification_topic).replace("{CLIENT_ID}", client_id)

    response = httpx.post(
        url="http://localhost:3000/api/v1/provisioning/alert-rules",
        json=json.loads(request), headers={
            "Authorization": "Bearer glsa_Dx4X1gQH0jQSS0I01Z9C6H4ppwm3Roj7_c4e1ab9a",
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    responst_data = response.json()
    if "message" in responst_data:
        print(responst_data)
        return True, response.json()["message"]
    return True, "Contact is created"


def toggle_alarm_rule(alarm_rule_id: str, status: bool):
    request = {"isPaused": status}

    response = httpx.put(
        url="http://localhost:3000/api/v1/provisioning/alert-rules/{alarm_rule_id}",
        json=request, headers={
            "Authorization": "Bearer glsa_Dx4X1gQH0jQSS0I01Z9C6H4ppwm3Roj7_c4e1ab9a",
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
    #print(delete_alarm_rule("edx095oz0zbb4a"))
