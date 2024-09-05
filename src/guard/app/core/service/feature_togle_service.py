from core.component.monitoring_component import get_chat_id, create_telegram_contact, delete_telegram_contact


def create_contact(user: str, chat_name: str, type: str):
    print("to create_contact:", user, chat_name, type)

    if type == "telegram" or "telegram" in type.lower():
        chat_id = get_chat_id(chat_name)
        if chat_id is not None:
            return create_telegram_contact(user, chat_id, chat_id)
        else:
            return False, f"Chat {chat_name} is not found"

    return False, f"Type {type} is unknown."


def delete_contact(user: str, chat_name: str, type: str):
    if type == "telegram" or "telegram" in type.lower():
        chat_id = get_chat_id(chat_name)
        if chat_id is not None:
            return delete_telegram_contact(user, chat_id)
        else:
            return False, f"Chat {chat_name} is not found"

    return False, f"Type {type} is unknown."
