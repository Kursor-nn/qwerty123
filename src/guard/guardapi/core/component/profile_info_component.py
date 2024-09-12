import httpx
from decouple import config

from auth.jwt_handler import create_access_token
from common_consts import BACKEND_HOST
from dto.ProfileDto import ProfileInfo


def __build_headers(user: str):
    token = create_access_token(user)
    headers = {"Authorization": f"Bearer {str(token)}", "Content-Type": "application/json"}

    return headers


def get_profile_info(user: str) -> ProfileInfo:
    response = httpx.get(url=f"{config(BACKEND_HOST)}/api/user/profile", headers=__build_headers(user))
    return ProfileInfo(**response.json())
