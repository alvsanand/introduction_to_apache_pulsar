import atexit
import json
import os
import logging
import pulsar
import time
from faker import Faker
import traceback

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


__PULSAR_URL = os.environ.get("PULSAR_URL", 'pulsar://localhost:6650')
__PULSAR_NAMESPACE = os.environ.get("PULSAR_NAMESPACE", 'tenant/namespace')
__TOPIC_NAME = os.environ.get("TOPIC_NAME", 'topic')
__TOPIC_URL = "persistent://{0}/{1}".format(__PULSAR_NAMESPACE, __TOPIC_NAME)
__PRODUCER_RATE = os.environ.get("PRODUCER_RATE", '10')


faker = Faker()


def generate_random_data():
    return {
        'transaction_id': faker.uuid4(),
        'date': faker.unix_time(),
        'credit_card_number': faker.iban(),
        'amount': faker.pyfloat(left_digits=3, right_digits=1, positive=True),
        'currency_code': faker.random_element(elements=('USD', 'EUR')),
    }


__running = True


def main():
    global __running

    logger.info("Init py-producer")

    client = pulsar.Client(__PULSAR_URL)
    producer = client.create_producer(__TOPIC_URL)

    rate = 1.0 / float(__PRODUCER_RATE)

    sent_msgs = 0

    while __running:
        json_data = generate_random_data()

        data = json.dumps(json_data).encode('utf-8')

        try:
            if sent_msgs % 50 == 0:
                logger.info("Already sent %d messages", sent_msgs)

            producer.send(data)
            sent_msgs = sent_msgs + 1
        except Exception:
            logger.error("Error sending data to Apache Pulsar")
            logging.error(traceback.format_exc())

        time.sleep(rate)

    producer.close()

    logger.info("Finished py-producer")


@atexit.register
def stop():
    global __running

    logger.info("Stopping py-producer")

    __running = False


if __name__ == "__main__":
    main()
