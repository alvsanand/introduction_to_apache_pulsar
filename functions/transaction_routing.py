from pulsar import Function
from _pulsar import CompressionType
import json


class TransactionRoutingFunction(Function):
    def __init__(self):
        pass

    def process(self, input, context):
        transaction = json.loads(input)

        topic = context.get_user_config_value('dollar_topic')
        if 'currency_code' in transaction and \
           transaction['currency_code'] == 'EUR':
            topic = context.get_user_config_value('euro_topic')

        context.publish(topic, input, compression_type=CompressionType.NONE)

        return
