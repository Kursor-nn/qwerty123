import json

from api.dto.message_request import ValidationResultMessage
from guardapi.core.queue.rabbitapi import send_message2rabbit


def validate(text: str) -> ValidationResultMessage:
    response = send_message2rabbit(text)
    return ValidationResultMessage(**json.loads(response))
