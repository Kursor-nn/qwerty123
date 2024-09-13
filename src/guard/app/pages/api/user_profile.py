import httpx
from decouple import config



from common_consts import BACKEND_HOST
from dto.ProfileDto import ProfileInfo
from pages.common.cookies import get_cookie_manager


def __build_headers():
    access_token = get_cookie_manager().get("access_token")
    headers = {"Authorization": f"Bearer {str(access_token)}", "Content-Type": "application/json"}

    return headers


def get_profile_info_for_user() -> ProfileInfo:
    response = httpx.get(url=f"{config(BACKEND_HOST)}/api/user/profile", headers=__build_headers())
    return ProfileInfo(**response.json())


def toggle_feature(feature_type_id: str, value: bool):
    data = {
        "feature_type_id": feature_type_id,
        "value": value,
        "chat_name": ""
    }
    res = httpx.post(url=f"{config(BACKEND_HOST)}/api/user/profile/feature", json=data, headers=__build_headers())
    return res.json()


def create_contact(type: str, address: str):
    data = {
        "chat_name": address,
    }
    res = httpx.post(url=f"{config(BACKEND_HOST)}/api/features/{type.lower()}", json=data, headers=__build_headers())
    return res.json()


def set_config(feature_type_id: str, value: str):
    data = {
        "config": value,
        "chat_name": value,
    }
    res = httpx.post(url=f"{config(BACKEND_HOST)}/api/features/{feature_type_id}/config",
                     json=data,
                     headers=__build_headers())

    return res.json()


def password_entered(login, password):
    data = {
        "login": login,
        "password": password
    }
    headers = {'Content-type': 'application/json'}
    res = httpx.post(url=f"{config(BACKEND_HOST)}/api/user/signin", json=data, headers=headers)
    return res


def create_user(login, user_password, email_address):
    data = {
        "login": login,
        "password": user_password,
        "email": email_address,
    }

    headers = {'Content-type': 'application/json'}
    res = httpx.post(url=f"{config(BACKEND_HOST)}/api/user/register", json=data, headers=headers)
    return res
