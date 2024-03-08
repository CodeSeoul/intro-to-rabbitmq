#!/usr/bin/env python
import random
import signal
from time import sleep
import pika


def main():
    print("starting")
    connection = pika.BlockingConnection(pika.ConnectionParameters("mq"))
    channel = connection.channel()
    exchange_name = 'languages'
    channel.exchange_declare(exchange=exchange_name,
                             exchange_type="topic")
    
    formats = ('digital', 'physical')
    languages = ('english', 'korean')

    running = True

    def signal_handler(*_):
        print("detected termination signal")
        nonlocal running 
        running = False

    signal.signal(signal.SIGINT, signal_handler)

    print("starting message loop")
    while running:
        send_message(exchange_name, channel, formats, languages)
        sleep(1)
    
    channel.close()
    print("connection closed")


def send_message(
        exchange_name: str,
        channel,  # BlockingChannel isn't exported. I'm sad
        formats: tuple[str, ...],
        languages: tuple[str, ...]
        ):
    selected_format = random.choice(formats)
    selected_language = random.choice(languages)

    if selected_language == "english":
        message = "hello"
    elif selected_language == "korean":
        message = "안녕하세요"
    else:
        raise NotImplementedError(f"Encountered unsupported language: {selected_language}")
    
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=f"{selected_format}.{selected_language}",
        body=message
    )
    print(f"sent message \"{message}\"!")


if __name__ == "__main__":
    main()
