from loguru import logger
from prometheus_client import Counter

from core.component import validate_component, llm_api
from dto.api_dto import ValidationResultsDto, FilterResultDto
from dto.llm_api import LlmAnswerDto
from dto.message_request import ValidationResultMessage

all_texts = Counter('input_text', 'Number of all requests', labelnames=["toxic_client_id"])
toxic_text = Counter('input_toxic_text', 'Number of toxic requests', labelnames=["toxic_client_id"])


def validate(user: str, text: str, rec_mode: bool, input_filters: [str], output_filters: [str]) -> ValidationResultsDto:
    results: ValidationResultMessage = validate_component.validate(user, input_filters, text)
    all_texts.labels(user).inc()

    logger.info(f"Validate text for user '{user}' for '{input_filters}' and '{output_filters}' and is toxic: '{results.is_toxic}'")

    if results.is_toxic:
        toxic_text.labels(user).inc()

    if rec_mode or not results.is_toxic:
        response: LlmAnswerDto = llm_api.ask_yandex(text, user)
        output: ValidationResultMessage = validate_component.validate(user, output_filters, response.text)

        llm_answer = "неприемлемы ответ от AI" if (output.is_toxic and not rec_mode) else response.text

        return ValidationResultsDto(is_toxic=results.is_toxic, question=text, llm_answer=llm_answer, details=[],
                                    answer_validation=[FilterResultDto(is_toxic=output.is_toxic, details=output.details)],
                                    input_validation=[FilterResultDto(is_toxic=results.is_toxic, details=results.details)])

    return ValidationResultsDto(is_toxic=results.is_toxic, question=text, llm_answer="Неприемлемый запрос.",
                                input_validation=[FilterResultDto(is_toxic=results.is_toxic, details=results.details)])
