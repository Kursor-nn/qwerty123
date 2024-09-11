import pika
from loguru import logger
from pika.adapters.blocking_connection import BlockingChannel


def build_rabbit_channel(host, port, user, password, queue, callback) -> BlockingChannel:
    logger.info(f"Run gpt-adapter queue '{queue}' handler: {user}@{host}:{port}")

    rabbitmq_connection_string = pika.ConnectionParameters(
        host=host,
        port=port,
        virtual_host='/',
        credentials=pika.PlainCredentials(
            username=user,
            password=password
        ),
        heartbeat=30,
        blocked_connection_timeout=2
    )

    connection = pika.BlockingConnection(rabbitmq_connection_string)
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    channel.basic_consume(
        queue=queue,
        on_message_callback=callback,
        auto_ack=False,
    )

    return channel
