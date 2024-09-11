import httpx
import loguru
from decouple import config

from common_consts import BACKEND_HOST
from pages.common.cookies import get_cookie_manager


def __build_headers():
    access_token = get_cookie_manager().get("access_token")
    headers = {"Authorization": f"Bearer {str(access_token)}", "Content-Type": "application/json"}

    return headers


def filter_validation(filter_type: str, text: str):
    data = {"text": text, "filter_type": filter_type}
    response = httpx.post(url=f"{config(BACKEND_HOST)}/api/guard/validate", json=data, headers=__build_headers(), timeout=60.0)
    return response.json()
