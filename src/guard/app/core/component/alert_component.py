import json

import httpx

from core.component.alarm_rules_templates import alert_template


def delete_alarm_rule(rule_id: str):
    response = httpx.delete(
        url=f"http://localhost:3000/api/v1/provisioning/alert-rules/{rule_id}",
        headers={
            "Authorization": "Bearer glsa_dSjUgivoAnnefXfX7exrlnBEe86Jde7j_77f253e4",
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    #responst_data = response.json()
    #if "message" in responst_data:
        #return True, response.json()["message"]
    return response.status_code in (204, 500), "Rule is removed"


def create_alarm_rule(rule_id: str, rule_title: str, notification_topic: str):
    request = alert_template.replace("{USER-ALERT-RULE-ID}", rule_id).replace("{USER-ALERT-TITLE-ID}", rule_title).replace(
        "{USER-NOTIFICAITON-ID}", notification_topic)

    response = httpx.post(
        url="http://localhost:3000/api/v1/provisioning/alert-rules",
        json=json.loads(request), headers={
            "Authorization": "Bearer glsa_dSjUgivoAnnefXfX7exrlnBEe86Jde7j_77f253e4",
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
    ))
    #print(delete_alarm_rule("edx095oz0zbb4a"))
