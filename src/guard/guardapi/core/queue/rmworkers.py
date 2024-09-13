import json
import logging

import pika
from core.component.mldp import binary_filter_v2, topic_detector_v2
from decouple import config
from pydantic import ValidationError

from common_consts import RABBIT_QUEUE
from dto.message_request import ValidationMessage

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
        logging.info(body.decode('utf-8'))
        info = ValidationMessage(**json.loads(body.decode('utf-8')))
        results = {}
        is_toxic = False
        for filter in info.filters:
            if filter == "general_filter":
                toxic_status, text = binary_filter_v2.check_toxic(info.text)
                results[filter] = toxic_status
                is_toxic = is_toxic or toxic_status
                logging.info(f"{filter} : {is_toxic} {toxic_status}")
            elif filter == "topic_detector":
                topic, text = topic_detector_v2.check_toxic(info.text)
                results[filter] = topic
                logging.info(f"{filter} : {is_toxic} {topic}")

        return_results(ch, method, properties, is_toxic, results)
    except ValidationError as e:
        correlation_id = properties.correlation_id
        reply_to = properties.reply_to
        logging.error(e)
        ch.basic_publish(
            exchange='',
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=json.dumps({"is_toxic": False, "message": "validation error"})
        )
    except Exception as e:
        correlation_id = properties.correlation_id
        reply_to = properties.reply_to
        logging.error(e)
        ch.basic_publish(
            exchange='',
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=json.dumps({"is_toxic": False, "message": "common error"})
        )


def return_results(ch, method, properties, toxic_status, text):
    correlation_id = properties.correlation_id
    reply_to = properties.reply_to

    ch.basic_publish(
        exchange='',
        routing_key=reply_to,
        properties=pika.BasicProperties(correlation_id=correlation_id),

        body=json.dumps({"is_toxic": toxic_status, "details": text})
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
