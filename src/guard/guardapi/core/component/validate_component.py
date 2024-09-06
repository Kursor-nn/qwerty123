import json

from core.queue.rabbitapi import send_message2rabbit
from dto.message_request import ValidationResultMessage


def validate(text: str) -> ValidationResultMessage:
    response = send_message2rabbit(text)
    return ValidationResultMessage(**json.loads(response))
