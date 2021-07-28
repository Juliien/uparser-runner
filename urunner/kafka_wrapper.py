import os
import json
import logging

from kafka import KafkaConsumer, KafkaProducer

# kafka default config, you can override this by setting INPUT_SERVER, INPUT_TOPIC and OUTPUT_SERVER to your environment
cfg = {'input': {'topic': 'runner-input', 'server': "localhost:9092"},
       'output': {'topic': 'runner-output', 'server': 'localhost:9092'}}


class Consumer:
    def __init__(self, logger=None):

        if logger:
            self.Logger = logger
        else:
            self.Logger = logging.getLogger()
            self.Logger.setLevel(logging.INFO)

        self.Logger.info("kafka consumer setup start")

        if "INPUT_SERVER" in os.environ:
            self.input_server = os.environ['INPUT_SERVER']
        else:
            self.input_server = cfg['input']['server']

        if 'INPUT_TOPIC' in os.environ:
            self.input_topic = os.environ['INPUT_TOPIC']
        else:
            self.input_topic = cfg['input']['topic']

        self.consumer = ""
        self.setup_kafka_consumer()
        self.Logger.info("kafka consumer setup end")

    def setup_kafka_consumer(self):
        self.consumer = KafkaConsumer(self.input_topic, bootstrap_servers=[self.input_server],
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

        if 'OUTPUT_SERVER' in os.environ:
            self.output_server = os.environ['OUTPUT_SERVER']
        else:
            self.output_server = cfg['output']['server']

        self.producer = ""
        self.setup_kafka_producer()
        self.Logger.info("kafka producer setup end")

    def setup_kafka_producer(self):
        self.producer = KafkaProducer(bootstrap_servers=[self.output_server],
                                      value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    def __del__(self):
        pass


