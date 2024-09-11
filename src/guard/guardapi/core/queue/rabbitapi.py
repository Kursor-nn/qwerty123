import uuid

import pika
from decouple import config

from common_consts import RABBIT_HOST, RABBIT_PORT, RABBIT_USER, RABBIT_PASSWORD
from dto.llm_api import LlmRequestDto

from loguru import logger

rabbitmq_connection_string = pika.ConnectionParameters(
    host=config(RABBIT_HOST),
    port=config(RABBIT_PORT),
    virtual_host='/',
    credentials=pika.PlainCredentials(
        username=config(RABBIT_USER),
        password=config(RABBIT_PASSWORD)
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)


def send_message(queue: str, request: LlmRequestDto) -> str:
    response = None
    connection = pika.BlockingConnection(rabbitmq_connection_string)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    result_queue = channel.queue_declare(queue='', exclusive=True).method.queue
    correlation_id = str(uuid.uuid4())
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        properties=pika.BasicProperties(reply_to=result_queue,
                                        correlation_id=correlation_id),
        body=request.model_dump_json())

    def on_response(ch, method, properties, body):
        if properties.correlation_id == correlation_id:
            channel.basic_cancel(consumer_tag=consumer_tag)
        channel.queue_delete(queue=result_queue)
        connection.close()
        nonlocal response
        response = body.decode('utf-8')

    consumer_tag = channel.basic_consume(queue=result_queue, on_message_callback=on_response, auto_ack=True)
    channel.start_consuming()
    return response
