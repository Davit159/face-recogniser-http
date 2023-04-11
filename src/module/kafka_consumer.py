import json

from confluent_kafka import Consumer, KafkaError


class KafkaMessage:
    def __init__(self, message):
        self.__message = message

    @classmethod
    def from_json(cls, message: str):
        return cls(json.loads(message))

    def to_json(self):
        return json.dumps(self.__message)

    def get_message(self):
        return self.__message

    def set_message(self, message: object):
        self.__message = message


class KafkaConsumer:
    def __init__(self, configuration, topic: list):
        self.consumer = Consumer(configuration)
        self.consumer.subscribe(topic)
        self.running = False

    def consume(self, consumer_function):
        self.running = True
        try:
            while self.running:
                msg = self.consumer.poll()
                if not msg.error():
                    value = msg.value().decode('utf-8')
                    consumer_function(KafkaMessage.from_json(value))
                elif msg.error().code() != KafkaError._PARTITION_EOF:
                    print(msg.error())
                    self.running = False
            self.consumer.close()
        except KeyboardInterrupt:
            self.consumer.close()
            pass