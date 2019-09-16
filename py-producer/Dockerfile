FROM python:3.6

COPY requirements.txt /

ENV "PULSAR_URL"="pulsar://localhost:6650" \
    "PULSAR_NAMESPACE"="tenant/namespace" \
    "TOPIC_NAME"="topic" \
    "TOPIC_SUBSCRIPTION"="subscription" \
    "PRODUCER_RATE"="100"

RUN pip install -r requirements.txt

COPY producer.py receiver.py /


CMD [ "python", "./producer.py" ]