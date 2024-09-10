import json
import uuid

import pika
from decouple import config

from common_consts import RABBIT_QUEUE

rabbitmq_connection_string = pika.ConnectionParameters(
    host="rabbitmq",
    port=5672,
    virtual_host='/',
    credentials=pika.PlainCredentials(
        username="admin",
        password="admin"
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)


def send_message2rabbit(filter_type: str, message: str) -> str:
    response = None
    connection = pika.BlockingConnection(rabbitmq_connection_string)
    channel = connection.channel()
    queue_name = config(RABBIT_QUEUE)
    channel.queue_declare(queue=queue_name)
    result_queue = channel.queue_declare(queue='', exclusive=True).method.queue
    correlation_id = str(uuid.uuid4())
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        properties=pika.BasicProperties(reply_to=result_queue,
                                        correlation_id=correlation_id),
        body=json.dumps({
            "type": filter_type,
            "message": message
        }))

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
