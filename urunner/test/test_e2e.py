from urunner.kafka_wrapper import Producer
from urunner.tools import kafka_mock


if __name__ == "__main__":
    producer = Producer()
    data = kafka_mock()
    producer.producer.send("runner-input", data).get()
    print('lmao')
