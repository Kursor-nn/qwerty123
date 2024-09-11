from fastapi import APIRouter, Depends

from api.dto.ProfileDto import ProfileInfo
from api.dto.features_dto import FeatureToggleDto
from auth.authenticate import authenticate
from core.component.profile_component import get_features, toggle_feature
from core.service.user_service import create_new_user, signin
from dto.user_dto import NewUser, SuccessResponse, TokenResponse, SigninRequest

user_router = APIRouter(tags=["User"])


@user_router.post("/register", response_model=SuccessResponse)
async def create_new_user(
        user: NewUser
) -> SuccessResponse:
    return create_new_user(user.login, user.password, user.email)


@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(
        request: SigninRequest
) -> dict:
    return signin(request.login, request.password)


@user_router.get("/profile", response_model=ProfileInfo)
async def profile(
        user: str = Depends(authenticate)
) -> ProfileInfo:
    return ProfileInfo(
        username=user, features=[data.__dict__ for data in get_features(user)]
    )


@user_router.post("/profile/feature", status_code=200)
async def profile(
        feature_toggle: FeatureToggleDto,
        user: str = Depends(authenticate)
):
    toggle_feature(user, feature_toggle.feature_type_id, feature_toggle.value)
