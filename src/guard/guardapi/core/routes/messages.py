from fastapi import APIRouter, HTTPException, status
from prometheus_client import Counter

from api.dto.api_dto import InputTextDto, ValidationResultsDto, FilterResultDto
from guardapi.core.component import filter_component

input_validation_requests = Counter('input_validation_requests', 'Input validation requests')
toxic_text = Counter('input_toxic_text', 'Number of toxic requests')

message_router = APIRouter(tags=["Messages"])

EMAIL_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User with email provided exists already.",
)

REG_REQUEST_IS_BROKEN = HTTPException(
    status_code=400, detail="Login, Email and password must be filled",
)

USER_IS_NOT_EXIST = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
)

USER_CREDS_ARE_WRONG = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details passed."
)


@message_router.post("/validate", response_model=ValidationResultsDto)
async def validate(
        request: InputTextDto
) -> ValidationResultsDto:
    input_validation_requests.inc()

    results = filter_component.validate(request.text)

    if results.is_toxic:
        toxic_text.inc()

    return ValidationResultsDto(is_toxic=results.is_toxic, details=[
        FilterResultDto(is_toxic=results.is_toxic, name=results.filter)
    ])
