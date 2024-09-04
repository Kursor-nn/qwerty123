from typing import Union

from pydantic import BaseModel


class NewUser(BaseModel):
    login: str
    email: str
    password: str

    def __init__(self, **data):
        super().__init__(**data)
        self.password = data["password"]
        self.email = data["email"]
        self.login = data["login"]


class SuccessResponse(BaseModel):
    message: Union[str, None] = None


class SigninRequest(BaseModel):
    login: Union[str, None] = None
    password: Union[str, None] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.password = data["password"]
        self.login = data["login"]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    def __init__(self, **data):
        super().__init__(**data)
        self.access_token = data['access_token']
        self.token_type = data['token_type']
