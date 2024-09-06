import httpx


def get_chat_id(chat_name):
    response = httpx.get(url="https://api.telegram.org/bot7079427253:AAEVbRwJE5yXE7mnGhS9Ayk4z8MoAiRXXb0/getUpdates")
    chats = response.json()["result"]
    target_chat = [char for char in chats if "my_chat_member" in char is not None if char["my_chat_member"]["chat"]["title"] == chat_name]

    target_chat_id = None
    if target_chat is None or len(target_chat) == 0:
        target_chat_id = [char["channel_post"]["sender_chat"]["id"] for char in chats if "channel_post" in char is not None if
                          char["channel_post"]["sender_chat"]["title"] == chat_name][0]
    else:
        target_chat_id = target_chat[0]["my_chat_member"]["chat"]["id"]

    return target_chat_id


def create_telegram_contact(contact_name: str, chat_id: str):
    contact_id = f"{contact_name}-{chat_id}"

    """
curl -X POST -H "Content-Type:application/json" -d  "{"chat_id": ""-1002200300374"", "text":"Что-то произошло в гарде", "disable_notification":true}" https://api.telegram.org/bot7079427253:AAEVbRwJE5yXE7mnGhS9Ayk4z8MoAiRXXb0/sendMessage
"""

    url = "https://api.telegram.org/bot7079427253:AAEVbRwJE5yXE7mnGhS9Ayk4z8MoAiRXXb0/sendMessage"

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
        url="http://grafana:3000/api/v1/provisioning/contact-points",
        json=data, headers={
            "Authorization": "Bearer glsa_cC4xIK7hKEihugIRFWomje7cLe2jTQBt_46984faa",
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    responst_data = response.json()
    if "message" in responst_data:
        return True, response.json()["message"], contact_id
    return True, "Contact is created", contact_id


def delete_telegram_contact(contact_name: str, chat_id: str):
    response = httpx.delete(
        url=f"http://grafana:3000/api/v1/provisioning/contact-points/{contact_name}-{chat_id}",
        headers={
            "Authorization": "Bearer glsa_cC4xIK7hKEihugIRFWomje7cLe2jTQBt_46984faa",
            "accept": "application/json",
            "Content-Type": "application/json"
        })

    return (True, response.json()["message"])


def create_email_contact(contact_name: str, chat_id: str):
    pass


if __name__ == "__main__":
    test = {"ok": True, "result": [{"update_id": 799267549,
                                    "channel_post": {"message_id": 3,
                                                     "sender_chat": {"id": -1002200300374, "title": "#\u0439\u0443\u043a\u0435\u043d123",
                                                                     "type": "channel"},
                                                     "chat": {"id": -1002200300374, "title": "#\u0439\u0443\u043a\u0435\u043d123",
                                                              "type": "channel"}, "date": 1725607789, "text": "test"}}]}
    value = [char for char in test["result"] if "channel_post" in char is not None if
             char["channel_post"]["sender_chat"]["title"] == "#йукен123"]

    print(value[0])
