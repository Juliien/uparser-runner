from kafka import KafkaConsumer, KafkaProducer
from urunner.tools import kafka_mock

import json

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    data = kafka_mock()
    producer.send("runner-input", data).get()
    print('lmao')
