import loguru
from fastapi import HTTPException, Depends, status

from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from core.component import user_component as UserComponent
from core.component.alert_component import create_alarm_rule, delete_alarm_rule
from core.component.profile_component import get_feature_by_id
from core.component.user_component import get_user_by_login
from core.database.database import get_session
from core.service.feature_togle_service import create_contact
from dto.user_dto import SuccessResponse

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


def create_new_user(
        login: str,
        password: str,
        email: str,
        session=get_session()
) -> SuccessResponse:
    if UserComponent.get_user_email(email, session):
        raise EMAIL_EXISTS

    if login is None or email is None or password is None:
        raise REG_REQUEST_IS_BROKEN

    hashed_password = hash_password.create_hash(password)
    password = hashed_password

    UserComponent.add_client(
        login, email, password, session
    )

    return SuccessResponse(message="User created successfully.")


def signin(login: str, password: str, session=get_session()):
    user_exist = get_user_by_login(login, session)

    if user_exist is None: raise USER_IS_NOT_EXIST

    if hash_password.verify_hash(password, user_exist.password):
        access_token = create_access_token(user_exist.login)
        return {"access_token": access_token, "token_type": "Bearer"}

    loguru.logger.info("USER_CREDS_ARE_WRONG > " + str(USER_CREDS_ARE_WRONG))
    raise USER_CREDS_ARE_WRONG


def toggle_feature(user: str, feature_type_id: str, feature_status: bool):
    feature = get_feature_by_id(user, feature_type_id)
    _, _, contact_id = create_contact(user, feature.config, feature.name)
    if contact_id:
        if feature_status:
            _, _, rule_id = create_alarm_rule(f"{user}-toxic-threshold-notification",
                                              f"{user}-toxic-threshold-notification",
                                              contact_id + "-notification", user)
        else:
            delete_alarm_rule(f"{user}-toxic-threshold-notification")

    toggle_feature(user, feature_type_id, feature_status)
