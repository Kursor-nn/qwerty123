import httpx
from decouple import config

from core.cookies.cookies import get_cookie_manager
from utils.const import BACKEND_HOST


def __build_headers():
    access_token = get_cookie_manager().get("access_token")
    headers = {"Authorization": f"Bearer {str(access_token)}", "Content-Type": "application/json"}

    return headers


def filter_validation(text: str):
    data = {"text": text}
    response = httpx.post(url=f"{config(BACKEND_HOST)}/api/guard/validate", json=data, headers=__build_headers(), timeout=60.0)
    return response.json()
