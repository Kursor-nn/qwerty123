import time
from datetime import datetime

import loguru
from decouple import config
from fastapi import HTTPException, status
from jose import jwt, JWTError

SECRET_KEY = config("SECRET_KEY")


def create_access_token(user: str) -> str:
    loguru.logger.info(f"SECRET_KEY > {SECRET_KEY}")
    payload = {"user": user, "expires": time.time() + 3600}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_access_token(token: str) -> dict:
    try:
        loguru.logger.info(f"SECRET_KEY > {SECRET_KEY}")
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied",
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token expired!"
            )
        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

