import loguru
from fastapi import APIRouter, Depends

from auth.authenticate import authenticate
from core.component.profile_component import get_features, toggle_feature
from core.service.user_service import create_new_user, signin
from dto.ProfileDto import ProfileInfo
from dto.features_dto import FeatureToggleDto
from dto.user_dto import NewUser, SuccessResponse, TokenResponse, SigninRequest


import core.service.user_service
user_router = APIRouter(tags=["User"])


@user_router.post("/register", response_model=SuccessResponse)
async def registration(
        user: NewUser
) -> SuccessResponse:
    return create_new_user(user.login, user.password, user.email)


@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(
        request: SigninRequest
) -> dict:
    loguru.logger.info(f"{request.login}, {request.password}")
    return signin(request.login, request.password)


@user_router.get("/profile", response_model=ProfileInfo)
async def profile(
        user: str = Depends(authenticate)
) -> ProfileInfo:
    return ProfileInfo(
        username=user, features=[data.__dict__ for data in get_features(user)]
    )


@user_router.get("/profile/features/{type}", response_model=ProfileInfo)
async def profile(
        type: str,
        user: str = Depends(authenticate)
) -> ProfileInfo:
    return ProfileInfo(
        username=user, features=[data.__dict__ for data in get_features(user) if data.name == type]
    )


@user_router.post("/profile/feature", status_code=200)
async def profile(
        feature_toggle: FeatureToggleDto,
        user: str = Depends(authenticate)
):
    toggle_feature(user, feature_toggle.feature_type_id, feature_toggle.value)
