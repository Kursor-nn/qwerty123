import json

import pika
from decouple import config
from pydantic import ValidationError

from common_consts import RABBIT_QUEUE
from core.component import catboost_bert_toxic_service

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
        toxic_status, text = catboost_bert_toxic_service.check_toxic(body.decode('utf-8'))
        return_results(ch, method, properties, toxic_status, text)
    except ValidationError as e:
        correlation_id = properties.correlation_id
        reply_to = properties.reply_to
        ch.basic_publish(
            exchange='',
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=json.dumps({"is_toxic": False, "filter": "validation error"})
        )
    except Exception as e:
        correlation_id = properties.correlation_id
        reply_to = properties.reply_to
        ch.basic_publish(
            exchange='',
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=json.dumps({"is_toxic": False, "filter": "common error "})
        )


def return_results(ch, method, properties, toxic_status, text):
    correlation_id = properties.correlation_id
    reply_to = properties.reply_to

    ch.basic_publish(
        exchange='',
        routing_key=reply_to,
        properties=pika.BasicProperties(correlation_id=correlation_id),

        body=json.dumps({"is_toxic": toxic_status, "filter": text})
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
