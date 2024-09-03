from fastapi import APIRouter, HTTPException, Depends, status

from core.auth.hash_password import HashPassword
from core.auth.jwt_handler import create_access_token
from core.component import user_component as UserComponent
from core.database.database import get_session
from core.routes.dto.RegUserDto import NewUser, SuccessResponse, TokenResponse, SigninRequest

user_router = APIRouter(tags=["User"])
hash_password = HashPassword()

EMAIL_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User with email provided exists already.",
)

REG_REQUEST_IS_BROKEN = HTTPException(
    status_code=400,
    detail="Login, Email and password must be filled",
)

USER_IS_NOT_EXIST = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
)

USER_CREDS_ARE_WRONG = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details passed."
)


@user_router.post("/register", response_model=SuccessResponse)
async def sign_new_user(
        user: NewUser,
        session=Depends(get_session)
) -> SuccessResponse:
    if UserComponent.get_user_email(user.email, session):
        raise EMAIL_EXISTS

    if user.login is None or user.email is None or user.password is None:
        raise REG_REQUEST_IS_BROKEN

    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password

    UserComponent.add_client(
        user.login, user.email, user.password, session
    )

    return SuccessResponse(message="User created successfully.")


@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(
        request: SigninRequest,
        session=Depends(get_session)
) -> dict:
    user_exist = UserComponent.get_user_by_login(request.login, session)

    if user_exist is None: raise USER_IS_NOT_EXIST

    if hash_password.verify_hash(request.password, user_exist.password):
        access_token = create_access_token(user_exist.login)
        return {"access_token": access_token, "token_type": "Bearer"}

    raise USER_CREDS_ARE_WRONG
