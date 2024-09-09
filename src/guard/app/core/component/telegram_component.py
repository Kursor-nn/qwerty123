import httpx
from decouple import config

from common_consts import TELEGRAM_BOT_TOKEN

telegram_token_with_prefix = config(TELEGRAM_BOT_TOKEN)


def get_chat_id(chat_name):
    if chat_name is None:
        return None
    response = httpx.get(url=f"https://api.telegram.org/{telegram_token_with_prefix}/getUpdates")
    chats = response.json()["result"]
    target_chat = [char for char in chats if "my_chat_member" in char is not None if char["my_chat_member"]["chat"]["title"] == chat_name]

    target_chat_id = None
    if target_chat is None or len(target_chat) == 0:
        char = [char["channel_post"]["sender_chat"]["id"] for char in chats if "channel_post" in char is not None if
                char["channel_post"]["sender_chat"]["title"] == chat_name]

        if len(char) == 0: return None
        target_chat_id = char[0]
    else:
        target_chat_id = target_chat[0]["my_chat_member"]["chat"]["id"]

    return target_chat_id
