from fastapi import APIRouter, HTTPException, status, Depends
from prometheus_client import Counter

from auth.authenticate import authenticate
from core.component import validate_component
from dto.alerts import AlertMessage
from dto.api_dto import InputTextDto, ValidationResultsDto, FilterResultDto

# registry = CollectorRegistry()


all_texts = Counter('input_text', 'Number of all requests', labelnames=["toxic_client_id"])
toxic_text = Counter('input_toxic_text', 'Number of toxic requests', labelnames=["toxic_client_id"])

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


@message_router.post("/check", response_model=ValidationResultsDto)
async def validate(
        alarm: AlertMessage
) -> ValidationResultsDto:
    return ValidationResultsDto(is_toxic=False, details=[
        FilterResultDto(is_toxic=False, name="asdasd")
    ])


@message_router.post("/validate", response_model=ValidationResultsDto)
async def validate(
        request: InputTextDto,
        user: str = Depends(authenticate)
) -> ValidationResultsDto:
    results = validate_component.validate(request.text)
    all_texts.labels(user).inc()

    if results.is_toxic:
        toxic_text.labels(user).inc()

    return ValidationResultsDto(is_toxic=results.is_toxic, details=[
        FilterResultDto(is_toxic=results.is_toxic, name=results.filter)
    ])
