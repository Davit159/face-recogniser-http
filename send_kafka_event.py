from confluent_kafka import Producer
import time
import json
from random import choice
from string import ascii_lowercase
import ssl

sasl_mechanism = 'PLAIN'
security_protocol = 'SASL_SSL'

# Create a new context using system defaults, disable all but TLS1.2
context = ssl.create_default_context()
context.options &= ssl.OP_NO_TLSv1
context.options &= ssl.OP_NO_TLSv1_1

KAFKA_PRODUCER_CONFIGURATION = {
    'bootstrap.servers': 'localhost:9092',
    'message.max.bytes': 5242880,
    'security.protocol' : 'SASL_PLAINTEXT',
    'sasl.username': 'admin',
    'sasl.password': 'admin-secret',
    'sasl.mechanism':'PLAIN'
}

producer = Producer(KAFKA_PRODUCER_CONFIGURATION)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

lis = list(ascii_lowercase)
#long_ms = ''.join(choice(lis) for _ in range(1000000))

producer = Producer(KAFKA_PRODUCER_CONFIGURATION)
producer.flush()
for x in range(1):
    value = json.dumps({
        "name": f"Alfred {x}",
        "account_provider": "fb",
        "images": ['image.jpeg'],
        "account_id": "2141242432"
    })
    print(value)
    producer.produce('accounts', key="test1", value=value, callback=acked)
    time.sleep(1)


