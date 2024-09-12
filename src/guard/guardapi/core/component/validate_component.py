import json

import loguru
from core.queue.rabbitapi import send_message
from decouple import config

from common_consts import RABBIT_QUEUE
from dto.message_request import ValidationResultMessage, ValidationMessage


def validate(user: str, filters: [str], text: str) -> ValidationResultMessage:
    request = ValidationMessage(filters=filters, text=text, user=user)
    response = send_message(config(RABBIT_QUEUE), request)
    loguru.logger.info(f"Prepare validation request : {request} and get response: {response}")
    return ValidationResultMessage(**json.loads(response))
