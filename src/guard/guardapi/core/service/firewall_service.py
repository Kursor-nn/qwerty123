from loguru import logger
from prometheus_client import Counter

from core.component import validate_component, llm_api
from dto.api_dto import ValidationResultsDto, FilterResultDto

all_texts = Counter('input_text', 'Number of all requests', labelnames=["toxic_client_id"])
toxic_text = Counter('input_toxic_text', 'Number of toxic requests', labelnames=["toxic_client_id"])


def validate(user: str, text: str, filter: str) -> ValidationResultsDto:
    results = validate_component.validate(user, filter, text)
    all_texts.labels(user).inc()

    logger.info(f"Validate text for user '{user}' for '{filter}' and is toxic: '{results.is_toxic}'")

    if results.is_toxic:
        toxic_text.labels(user).inc()
    else:
        response = llm_api.ask_yandex(text, user)
        return ValidationResultsDto(is_toxic=results.is_toxic, llm_answer=response.text, details=[
            FilterResultDto(is_toxic=results.is_toxic, name=results.filter)
        ])

    return ValidationResultsDto(is_toxic=results.is_toxic, llm_answer="Неприемлемый запрос.", details=[
        FilterResultDto(is_toxic=results.is_toxic, name=results.filter)
    ])
