from fastapi import APIRouter, Depends

from api.dto.features_dto import FeatureConfigDto, OperationStatusResponseDto
from auth.authenticate import authenticate
from auth.hash_password import HashPassword
from core.component.profile_component import set_config_to
from core.service.feature_togle_service import create_contact

features_router = APIRouter(tags=["Features"])
hash_password = HashPassword()


@features_router.post("/{type}", status_code=200)
async def feature_config(
        type: str,
        config: FeatureConfigDto,
        user: str = Depends(authenticate)
):
    status, message = create_contact(user, config.chat_name, type)
    return OperationStatusResponseDto(status=status, details=message)


@features_router.post("/{feature_type_id}/config", status_code=200)
async def profile(
        feature_type_id: str,
        feature_config: FeatureConfigDto,
        user: str = Depends(authenticate)
):
    set_config_to(user, feature_type_id, feature_config.config)
