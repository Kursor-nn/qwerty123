from fastapi import APIRouter, Depends

from auth.authenticate import authenticate
from core.service import firewall_service
from dto.api_dto import InputTextDto, ValidationResultsDto

message_router = APIRouter(tags=["Messages"])


@message_router.post("/validate", response_model=ValidationResultsDto)
async def validate(
        request: InputTextDto,
        user: str = Depends(authenticate)
) -> ValidationResultsDto:
    return firewall_service.validate(user, request.text, [request.filter_type], ["topic_detector"])
