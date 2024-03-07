FROM python:3

WORKDIR /app

ADD . /app

RUN pip install .

ENTRYPOINT [ "python", "-m", "consumer.main" ]
