import json
import logging

from kafka import KafkaConsumer, KafkaProducer
from urunner.config.kafka_config import cfg


class Consumer:
    def __init__(self, logger=None):
        if logger:
            self.Logger = logger
        else:
            self.Logger = logging.getLogger()
            self.Logger.setLevel(logging.INFO)

        self.Logger.info("kafka consumer setup start")
        self.input = cfg['input']
        self.consumer = ""
        self.setup_kafka_consumer()
        self.Logger.info("kafka consumer setup end")

    def setup_kafka_consumer(self):
        self.consumer = KafkaConsumer(self.input['topic'], bootstrap_servers=[self.input['server']],
                                      auto_offset_reset='earliest',
                                      value_deserializer=lambda x: json.loads(x.decode('utf-8')), group_id='urunner-0')
        KafkaConsumer(consumer_timeout_ms=1000)

    def __del__(self):
        pass


class Producer:
    def __init__(self, logger=None):
        if logger:
            self.Logger = logger
        else:
            self.Logger = logging.getLogger()
            self.Logger.setLevel(logging.INFO)

        self.Logger.info("kafka producer setup start")
        self.output = cfg['output']
        self.producer = ""
        self.setup_kafka_producer()
        self.Logger.info("kafka producer setup end")

    def setup_kafka_producer(self):
        self.producer = KafkaProducer(bootstrap_servers=[self.output['server']],
                                      value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    def __del__(self):
        pass


