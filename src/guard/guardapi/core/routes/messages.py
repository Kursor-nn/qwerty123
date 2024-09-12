from fastapi import APIRouter, Depends

from auth.authenticate import authenticate
from core.service import firewall_service
from core.service.possible_filter_service import collect_filters
from dto.api_dto import InputTextDto, ValidationResultsDto

message_router = APIRouter(tags=["Messages"])


@message_router.post("/validate", response_model=ValidationResultsDto)
async def validate(
        request: InputTextDto,
        user: str = Depends(authenticate)
) -> ValidationResultsDto:
    rec_mode, input_filters, output_filters = collect_filters(user)
    return firewall_service.validate(user, request.text, rec_mode, input_filters, output_filters)
