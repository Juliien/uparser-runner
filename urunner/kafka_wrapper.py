import json
import logging

from kafka import KafkaConsumer, KafkaProducer
from urunner.config.kafka_config import cfg


class KafkaWrapper:
    consumer = None
    producer = None

    def __init__(self):
        logging.info("Global Kafka setup start")
        self.output_topic = cfg['output']['topic']
        self.setup_kafka_consumer()
        self.setup_kafka_producer()
        logging.info("Global Kafka setup end")

    def setup_kafka_consumer(self):
        logging.info("kafka consumer setup start")
        config = cfg['input']
        consumer = KafkaConsumer(config['topic'], bootstrap_servers=[config['server']], auto_offset_reset='earliest',
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        KafkaConsumer(consumer_timeout_ms=1000)
        logging.info("kafka consumer setup end")
        self.consumer = consumer

    def setup_kafka_producer(self):
        logging.info("kafka producer setup start")
        config = cfg['output']
        producer = KafkaProducer(bootstrap_servers=[config['server']],
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        logging.info("kafka producer setup end")
        self.producer = producer

    def __del__(self):
        pass


