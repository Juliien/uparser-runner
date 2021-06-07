import docker
import time
import datetime
import logging
import sys
import os
import shutil

from kafka import KafkaConsumer
from .tools import decode, encode, consume


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Urunner(metaclass=Singleton):
    def __init__(self):
        # settings internals values
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
        #     self.run(etc)

    def __del__(self):
        self.end_time = datetime.datetime.utcnow()
        logging.info("test ended: {}".format(datetime.datetime.utcnow()))

        self.run_time = self.end_time - self.start_time
        logging.info("test tun time: {}".format(self.run_time))

    # Mock func
    def idle(self):
        last_data = consume()
        if last_data:
            self.run(last_data['id'], last_data['from'], last_data['to'],
                     last_data['inputfile'], last_data['algorithm'], last_data['language'])
        else:
            time.sleep(1)

    # Main function
    def run(self, id, src, dest, inputfile, algorithm, language):
        logging.info("test started: {}".format(datetime.datetime.utcnow()))
        try:
            os.mkdir("./{}".format(id))
        except Exception as e:
            print("[ERROR] CREATING TMP FOLDER FAILED, DOCKER WONT ACCESS FILES!!! StackTrace: {}".format(e))

        os.chdir("./{}".format(id))
        self.create_files(src, inputfile, algorithm, language)
        os.chdir("..")
        results = self.run_docker(id, src, language)
        if not results:
            print("ERROR TO HANDLE")
        self.clean_host_files(id)
        self.produce(results)

    @staticmethod
    def run_docker(id, src, language):  # TODO adapt test_run.sh to docker.py lib
        run_cmd = ""
        if language == "python":
            run_cmd = [language, "code.py", "in.{}".format(src)]
        elif language == "c":
            run_cmd = ["./a.out"]
        client = docker.client.from_env()
        if run_cmd:
            test_run = client.containers.run("urunner:python3.8", run_cmd, detach=True, stdout=True)
            return test_run
        return None

    @staticmethod
    def clean_host_files(id):
        try:
            shutil.rmtree('./{}'.format(id), ignore_errors=False)
        except Exception as e:
            print(e)

    @staticmethod
    def create_files(src, inputfile, algorithm, language):
        # creating input file with right extension
        with open("in.{}".format(src), "w+") as data_to_parse:
            data_to_parse.write(decode(inputfile).decode('utf-8'))

        # creating code files
        if language == "python":
            with open("code.py", "w+") as code_to_run:
                code_to_run.write(decode(algorithm).decode('utf-8'))

    @staticmethod
    def produce(results):
        print(results)
        # TODO produce to kafka topic


# TODO Une image par techno ? avec urunner:python par exemple, comment faire pour le ENTRYPOINT alors ?
# TODO ? Build l'image au moment du run ?

