FROM python:3.6

COPY producer.py receiver.py requirements.txt /

ENV "PULSAR_URL"="pulsar://localhost:6650" \
    "PULSAR_NAMESPACE"="tenant/namespace" \
    "TOPIC_NAME"="topic" \
    "TOPIC_SUBSCRIPTION"="subscription" \
    "PRODUCER_RATE"="100"

RUN pip install -r requirements.txt

CMD [ "python", "./producer.py" ]