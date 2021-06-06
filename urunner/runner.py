import docker
import time
import datetime
import logging
import sys
import json

from kafka import KafkaConsumer
from .tools import decode, encode, consume

# ENV Values
RESSOURCES_DIR = "ressources/"
GENERATED_BY_USER_DIR = RESSOURCES_DIR + "generated_by_user/"
DESTINATION_PATHNAME_FORMAT = GENERATED_BY_USER_DIR + "{}"
MOCK_DIR = RESSOURCES_DIR + "mock_parsing_data/"
MOCK_JSON = "MOCK_DATA.json"
DESTINATION_NAME = ""


class Urunner:
    def __init__(self):
        # settings internals values
        self.dest_name = ""
        self.source_name = ""
        self.start_time = datetime.datetime.utcnow()

        # init logs
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        # connecting to kafka
        # topic = "uparser"
        # server = "localhost:9092"
        # group_id = "uparser"
        # self.consumer = KafkaConsumer(topic, bootstrap_servers=[server], auto_offset_reset='earliest',
        #                               enable_auto_commit=True, group_id=group_id,
        #                               value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        # KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)
        # KafkaConsumer(value_deserialize=lambda m: json.loads(m.decode('ascii')))
        # KafkaConsumer(consumer_timeout_ms=1000)
        # for message in self.consumer:
        #     print(message)
        #

    def __del__(self):
        self.end_time = datetime.datetime.utcnow()
        logging.info("test ended: {}".format(datetime.datetime.utcnow()))

        self.run_time = self.end_time - self.start_time
        logging.info("test tun time: {}".format(self.run_time))

    def idle(self):
        last_data = consume()
        if last_data:
            self.run(last_data['id'], last_data['from'], last_data['to'],
                     last_data['inputfile'], last_data['algorithm'], last_data['language'])
        else:
            time.sleep(1)

    def run(self, id, src, dest, inputfile, algorithm, language):
        logging.info("test started: {}".format(datetime.datetime.utcnow()))
        results = self.run_docker(id, src, dest, inputfile, algorithm, language)
        self.produce_results_for_kafka(results)

    def run_docker(self, id, src, dest, inputfile, algorithm, language):
        code_extension = 'py'
        client = docker.client.from_env()
        # run_cmd = "echo {} >> in.{};".format(decode(inputfile).decode('utf-8'), src)
        # run_cmd += "echo {} >> code.{};".format(decode(algorithm).decode('utf-8'), code_extension)
        # run_cmd += "{} code.{} in.{}".format(language, code_extension, src)
        test_run = client.containers.run("uparser-runner_runner-uwsgi", run_cmd, detach=True, stdout=True)
        print(test_run)
        return test_run

    def produce_results_for_kafka(self, results):
        print(results)
        pass
