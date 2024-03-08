#!/usr/bin/env python
import signal
import pika


def main():
    print("starting")
    connection = pika.BlockingConnection(pika.ConnectionParameters("mq"))
    channel = connection.channel()
    exchange_name = "languages"
    channel.exchange_declare(exchange=exchange_name, exchange_type="topic")
    
    queue_declare = channel.queue_declare("billing", durable=True)
    billing_queue_name = queue_declare.method.queue
    channel.queue_bind(
        exchange=exchange_name,
        queue=billing_queue_name,
        routing_key="*.*"
    )
    channel.basic_consume(
        queue=billing_queue_name,
        on_message_callback=billing_processor
    )

    queue_declare = channel.queue_declare("english", durable=True)
    english_queue_name = queue_declare.method.queue
    channel.queue_bind(
        exchange=exchange_name,
        queue=english_queue_name,
        routing_key="*.english"
    )
    channel.basic_consume(
        queue=english_queue_name,
        on_message_callback=english_processor
    )

    queue_declare = channel.queue_declare("korean", durable=True)
    korean_queue_name = queue_declare.method.queue
    channel.queue_bind(
        exchange=exchange_name,
        queue=korean_queue_name,
        routing_key="*.korean"
    )
    channel.basic_consume(
        queue=korean_queue_name,
        on_message_callback=korean_processor
    )

    def signal_handler(*_):
        print("detected termination signal")
        channel.stop_consuming()
        channel.close()
        print("consumption stopped and connection closed")

    signal.signal(signal.SIGINT, signal_handler)

    channel.start_consuming()


def billing_processor(channel, method, *_):
    format = method.routing_key.split(".")[0]
    if format == "digital":
        print("charging 100 KRW for digital card")
    elif format == "physical":
        print("charging 1000 KRW for physical card")
    else:
        raise NotImplementedError("Received invalid format")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def english_processor(channel, method, _, body: bytes):
    message = body.decode("UTF-8")
    print(f"creating English calligraphy design for message: \"{message}\"")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def korean_processor(channel, method, _, body: bytes):
    message = body.decode("UTF-8")
    print(f"creating Korean calligraphy design for message: \"{message}\"")
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    main()
