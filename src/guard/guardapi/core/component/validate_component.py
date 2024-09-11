import json

from core.queue.rabbitapi import send_message
from decouple import config

from common_consts import RABBIT_QUEUE
from dto.message_request import ValidationResultMessage, ValidationMessage


def validate(user: str, filter: str, text: str) -> ValidationResultMessage:
    response = send_message(config(RABBIT_QUEUE), ValidationMessage(type=filter, text=text, user=user))
    return ValidationResultMessage(**json.loads(response))
