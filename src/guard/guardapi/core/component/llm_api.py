import json

import httpx
from decouple import config
from fastapi import Depends

from auth.authenticate import oauth2_scheme_cookie
from common_consts import LLM_ADAPTER_ENDPOINT
from dto.llm_api import LlmAnswerDto

llm_adapter_endpoint = config(LLM_ADAPTER_ENDPOINT)
print("llm_adapter_endpoint", llm_adapter_endpoint)


def __headers(token: str):
    return {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        "Content-Type": "application/json"
    }


def ask_yandex(text: str, token: str = Depends(oauth2_scheme_cookie)) -> LlmAnswerDto:
    payload = {
        "text": text
    }

    response = httpx.post(
        url=f"{llm_adapter_endpoint}/api/llm/yandex_gpt/ask",
        json=payload,
        headers=__headers(token),
        timeout=60.0

    )

    return LlmAnswerDto(**response.json())
