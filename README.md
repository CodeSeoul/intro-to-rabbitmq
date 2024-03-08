# Intro to RabbitMQ

This repository is meant to be an introduction to [RabbitMQ](https://www.rabbitmq.com/) along with the [presentation](https://docs.google.com/presentation/d/19FAKNWsZJB6IqhR0u8ABbEZV3lnliz9mF5zQ9RTCxhY/edit?usp=sharing). **This is not production-ready.** This is purely for demonstrative purposes.

The main branch starts off with a blank workspace. Via [Docker Compose](https://docs.docker.com/compose/), we set up a single RabbitMQ instance, a producer container, and a consumer container. Currently, the producer and consumer only provide a print message to show they're running. RabbitMQ runs but without any configuration. Note that we're running RabbitMQ with the management plugin, which provides a UI to observe operations.

The `mq-config` branch includes configurations for RabbitMQ via a configuration file mounted into the Docker container. This branch demonstrates some configurations that can be done with RabbitMQ.

The `producer` branch includes everything in the `mq-config` branch plus a tiny application to push messages into RabbitMQ. The application is run inside the producer container using the Python client library.

The `consumer` branch includes everything in the `mq-config` branch plus a tiny application to consume messages from RabbitMQ. The application is run inside the producer container using the Python client library. Additionally, it shows how multiple consumer clients can pull from RabbitMQ to work in a distributed manner. This branch is considered the "final" version for demonstration.

## Running
```shell
docker compose up --build
```

## Checking
View RabbitMQ management interface on [localhost:8080](http://localhost:8080/). Default login is `guest` / `guest`.

## Cleanup
```shell
docker compose down
```
