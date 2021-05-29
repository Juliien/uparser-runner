from kafka import KafkaConsumer
import json


class KafkaWrapper:
    def __init__(self, topic="uparser", server="localhost:9092", groupid="uparser"):
        self.consumer = KafkaConsumer(topic, bootstrap_servers=[server], auto_offset_reset='earliest',
                                      enable_auto_commit=True, group_id=groupid,
                                      value_deserializer=lambda x: json.loads(x.decode('utf-8')))
