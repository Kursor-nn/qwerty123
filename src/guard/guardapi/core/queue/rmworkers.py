import json

import pika
from decouple import config
from pydantic import ValidationError

from api.const.const import RABBIT_QUEUE

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

MODEL_CACHE = {}

connection = pika.BlockingConnection(rabbitmq_connection_string)
channel = connection.channel()
channel.queue_declare(queue=config(RABBIT_QUEUE))


def prepare_data(ch, method, properties, body):
    try:
        return_results(ch, method, properties)
    except ValidationError as e:
        correlation_id = properties.correlation_id
        reply_to = properties.reply_to
        ch.basic_publish(
            exchange='',
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=json.dumps({"is_toxic": False, "filter": "error"})
        )


def return_results(ch, method, properties):
    correlation_id = properties.correlation_id
    reply_to = properties.reply_to

    ch.basic_publish(
        exchange='',
        routing_key=reply_to,
        properties=pika.BasicProperties(correlation_id=correlation_id),
        body=json.dumps({"is_toxic": False, "filter": "success"})
    )


def callback(ch, method, properties, body):
    prepare_data(ch, method, properties, body)


def start_consuming_ml():
    channel.basic_consume(
        queue=config(RABBIT_QUEUE),
        on_message_callback=callback,
        auto_ack=False,
    )
    channel.start_consuming()


if __name__ == "__main__":
    start_consuming_ml()
