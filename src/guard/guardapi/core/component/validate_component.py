import json

from core.queue.rabbitapi import send_message2rabbit
from dto.message_request import ValidationResultMessage


def validate(filter: str, text: str) -> ValidationResultMessage:
    response = send_message2rabbit(filter, text)
    return ValidationResultMessage(**json.loads(response))
