import httpx


def get_chat_id(chat_name):
    response = httpx.get(url="https://api.telegram.org/bot7079427253:AAEVbRwJE5yXE7mnGhS9Ayk4z8MoAiRXXb0/getUpdates")
    chats = response.json()["result"]
    target_chat = [char for char in chats if "my_chat_member" in char is not None if char["my_chat_member"]["chat"]["title"] == chat_name]

    target_chat_id = None
    if len(target_chat) > 0:
        target_chat_id = target_chat[0]["my_chat_member"]["chat"]["id"]

    return target_chat_id


def create_telegram_contact(contact_name: str, chat_name: str, chat_id: str):
    data = {
        "uid": f"{contact_name}-{chat_name}",
        "name": f"{contact_name}-{chat_name}-notification",
        "type": "webhook",
        "settings": {
            "httpMethod": "POST",
            "message": "{{ template \"default.message\" . }}",
            "title": "{{ template \"default.message\" . }}",
            "url": "http://llm-guardapi:8081/api/guard/check"
        },
        "disableResolveMessage": False
    }

    response = httpx.post(
        url="http://grafana:3000/api/v1/provisioning/contact-points",
        json=data, headers={
            "Authorization": "Bearer glsa_dSjUgivoAnnefXfX7exrlnBEe86Jde7j_77f253e4",
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    responst_data = response.json()
    if "message" in responst_data:
        return True, response.json()["message"]
    return True, "Contact is created"


def delete_telegram_contact(contact_name: str, chat_id: str):
    response = httpx.delete(
        url=f"http://grafana:3000/api/v1/provisioning/contact-points/{contact_name}-{chat_id}",
        headers={
            "Authorization": "Bearer glsa_dSjUgivoAnnefXfX7exrlnBEe86Jde7j_77f253e4",
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    return (True, response.json()["message"])


def create_email_contact(contact_name: str, chat_id: str):
    pass
