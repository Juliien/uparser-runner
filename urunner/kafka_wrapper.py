import json
import logging

from kafka import KafkaConsumer, KafkaProducer
from urunner.config.kafka_config import cfg


class KafkaWrapper:
    def __init__(self):
        logging.info("Global Kafka setup start")
        self.consumer = self.setup_kafka_consumer()
        self.producer = self.setup_kafka_producer()
        logging.info("Global Kafka setup end")

    @staticmethod
    def setup_kafka_consumer():
        logging.info("kafka consumer setup start")
        config = cfg['input']
        consumer = KafkaConsumer(config['topic'], bootstrap_servers=[config['server']], group_id=0,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))

        # KafkaConsumer(consumer_timeout_ms=1000)
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


