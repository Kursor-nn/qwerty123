import httpx
from decouple import config

from common_consts import GRAFANA_ENDPOINT, GRAFANA_SERVICE_TOKEN

grafana_endpoint = config(GRAFANA_ENDPOINT)
grafana_service_token = config(GRAFANA_SERVICE_TOKEN)

grafana_service_account_headers = {
    "Authorization": f"Bearer {grafana_service_token}",
    "accept": "application/json",
    "Content-Type": "application/json"
}

CREATE_NOTIFICATION_CONTACT_ENDPOINT = f"{grafana_endpoint}/api/v1/provisioning/contact-points"
DELETE_NOTIFICATION_CONTACT_ENDPOINT = f"{grafana_endpoint}/api/v1/provisioning/contact-points/"


def create_telegram_contact(contact_name: str, chat_id: str):
    contact_id = f"{contact_name}-{chat_id}"

    data = {
        "uid": f"{contact_id}",
        "name": f"{contact_name}-{chat_id}-notification",
        "type": "telegram",
        "settings": {
            "bottoken": "7079427253:AAEVbRwJE5yXE7mnGhS9Ayk4z8MoAiRXXb0",
            "chatid": str(chat_id),
            "disable_notification": False,
            "disable_web_page_preview": False,
            "message": "демократия в опасаности =)",
            "protect_content": False
        },
        "disableResolveMessage": False
    }

    response = httpx.post(
        url=CREATE_NOTIFICATION_CONTACT_ENDPOINT,
        json=data, headers=grafana_service_account_headers)

    payload = response.json()
    if "message" in payload:
        return True, payload["message"], contact_id
    return True, "Contact is created", contact_id


def delete_telegram_contact(contact_name: str, chat_id: str):
    contact_id = f"{contact_name}-{chat_id}"
    response = httpx.delete(
        url=DELETE_NOTIFICATION_CONTACT_ENDPOINT + contact_id,
        headers=grafana_service_account_headers)

    return True, response.json()["message"]
