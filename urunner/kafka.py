import json
import logging

from kafka import KafkaConsumer, KafkaProducer

INPUT_TOPIC = "uparser-input"
OUTPUT_TOPIC = "uparser-output"

server = "localhost:9092"
group_id = "uparser"


class KafkaWrapper:
    def __init__(self):
        logging.info("Global Kafka setup start")
        self.consumer = self.setup_kafka_consumer()
        self.producer = self.setup_kafka_producer()
        logging.info("Global Kafka setup end")

    @staticmethod
    def setup_kafka_consumer():
        logging.info("kafka consumer setup start")
        consumer = KafkaConsumer(INPUT_TOPIC, bootstrap_servers=[server], auto_offset_reset='earliest',
                                 enable_auto_commit=True, group_id=group_id,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))

        KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)
        KafkaConsumer(value_deserialize=lambda m: json.loads(m.decode('ascii')))
        KafkaConsumer(consumer_timeout_ms=1000)
        logging.info("kafka consumer setup end")
        return consumer

    @staticmethod
    def setup_kafka_producer():
        logging.info("kafka consumer setup start")
        producer = "dummy"
        logging.info("kafka consumer setup end")
        return producer

    def __del__(self):
        pass


