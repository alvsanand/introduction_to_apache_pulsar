import atexit
import json
import os
import logging
import pulsar
import traceback

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


__PULSAR_URL = os.environ.get("PULSAR_URL", 'pulsar://localhost:6650')
__PULSAR_NAMESPACE = os.environ.get("PULSAR_NAMESPACE", 'tenant/namespace')
__TOPIC_NAME = os.environ.get("TOPIC_NAME", 'topic')
__TOPIC_SUBSCRIPTION = os.environ.get("TOPIC_SUBSCRIPTION", 'subscription')
__TOPIC_URL = "persistent://{0}/{1}".format(__PULSAR_NAMESPACE, __TOPIC_NAME)


__running = True


def main():
    global __running

    logger.info("Init py-consumer")

    client = pulsar.Client(__PULSAR_URL)
    consumer = client.subscribe(__TOPIC_URL, __TOPIC_SUBSCRIPTION)

    while __running:
        try:
            data = consumer.receive()

            logging.info(json.loads(data.data()))
        except Exception:
            logger.error("Error receiving data to Apache Pulsar")
            logging.error(traceback.format_exc())

    consumer.close()

    logger.info("Finished py-consumer")


@atexit.register
def stop():
    global __consumer
    global __running

    logger.info("Stopping py-consumer")

    __running = False


if __name__ == "__main__":
    main()
