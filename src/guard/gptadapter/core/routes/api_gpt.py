from core.component.yandex_gpt_api import get_yandex_gpt_completion
from fastapi import APIRouter
from prometheus_client import Counter

from dto.llm_api import LlmAnswerDto, LlmRequestDto

llm_api_router = APIRouter(tags=["LLM Requests"])

all_request = Counter('llm_request', 'Number of all requests to llm', labelnames=["toxic_client_id", "llm_type_id"])
unknown_request = Counter('unknown_llm_type_request', 'Number of requests with unknown type', labelnames=["toxic_client_id", "llm_type_id"])


@llm_api_router.post("/{llm_type}/ask", response_model=LlmAnswerDto)
async def ask(
        llm_type: str,
        request: LlmRequestDto,
        # user: str = Depends(authenticate)
) -> LlmAnswerDto:
    user = "123123"
    if llm_type == "yandex_gpt":
        all_request.labels(user, llm_type).inc()
        result = await get_yandex_gpt_completion(request.text)
        return LlmAnswerDto(is_toxic=False, text=result)
    else:
        unknown_request.labels(user, llm_type).inc()
        return LlmAnswerDto(is_toxic=False, text=f"unknown llm type: {llm_type}", status="failed")
