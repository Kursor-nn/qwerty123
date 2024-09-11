import json

import loguru
from core.queue.rabbitapi import send_message
from decouple import config

from common_consts import LLM_ADAPTER_ENDPOINT, GPT_ADAPTER_QUEUE
from dto.llm_api import LlmAnswerDto, LlmRequestDto

llm_adapter_endpoint = config(LLM_ADAPTER_ENDPOINT)


def ask_yandex(text: str, user: str) -> LlmAnswerDto:
    response = send_message(config(GPT_ADAPTER_QUEUE), LlmRequestDto(text=text, user=user))
    return LlmAnswerDto(**json.loads(response))
