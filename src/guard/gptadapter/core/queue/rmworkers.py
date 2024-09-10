import json

import pika
from loguru import logger
from pydantic import ValidationError

from core.component import yandex_gpt_api
from dto.llm_api import LlmRequestDto, LlmAnswerDto
from service.rabbit_service import build_rabbit_channel


def prepare_data(ch, method, properties, body):
    try:
        request = LlmRequestDto(**json.loads(body.decode('utf-8')))
        logger.info(f"Invoke gpt llm for '{request.text}'")
        response = yandex_gpt_api.get_yandex_gpt_completion(request.text)
        return_results(ch, method, properties, LlmAnswerDto(text=response, is_toxic=False))
    except ValidationError as e:
        logger.info(f"Validation Error: {body.decode('utf-8')}", str(e))
        return_results(ch, method, properties, LlmAnswerDto(text=str(e), status="failed"))
    except Exception as e:
        logger.info(f"General Error: {body.decode('utf-8')}", str(e))
        return_results(ch, method, properties, LlmAnswerDto(text=str(e), status="failed"))


def return_results(ch, method, properties, response: LlmAnswerDto):
    correlation_id = properties.correlation_id
    reply_to = properties.reply_to

    ch.basic_publish(
        exchange='',
        routing_key=reply_to,
        properties=pika.BasicProperties(correlation_id=correlation_id),
        body=json.dumps(response)
    )


def callback(ch, method, properties, body):
    prepare_data(ch, method, properties, body)


async def run_adapter_queue_channel(host, port, user, password, queue):
    logger.info(f"Run gpt-adapter queue '{queue}' handler: {user}@{host}:{port}")
    channel = build_rabbit_channel(host, port, user, password, queue, callback)
    channel.start_consuming()
