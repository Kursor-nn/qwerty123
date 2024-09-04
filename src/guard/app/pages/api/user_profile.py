import httpx
from decouple import config

from api.dto.ProfileDto import ProfileInfo
from core.cookies.cookies import get_cookie_manager
from utils.const import BACKEND_HOST


def __build_headers():
    access_token = get_cookie_manager().get("access_token")
    headers = {"Authorization": f"Bearer {str(access_token)}", "Content-Type": "application/json"}

    return headers


def get_profile_info() -> ProfileInfo:
    response = httpx.get(url=f"{config(BACKEND_HOST)}/api/user/profile", headers=__build_headers())
    return ProfileInfo(**response.json())


def toggle_feature(feature_type_id: str, value: bool):
    data = {
        "feature_type_id": feature_type_id,
        "value": value
    }
    res = httpx.post(url=f"{config(BACKEND_HOST)}/api/user/profile/feature", json=data, headers=__build_headers())
    return res.json()
