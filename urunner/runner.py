import docker
import time
import datetime
import sys
import os
import shutil
import logging

from pprint import pprint

from tools import decode, encode, kafka_mock


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

        # kafka
        # backend_queue = KafkaWrapper()

    def __del__(self):
        self.end_time = datetime.datetime.utcnow()
        logging.info("test ended: {}".format(datetime.datetime.utcnow()))

        self.run_time = self.end_time - self.start_time
        logging.info("test tun time: {}".format(self.run_time))

    # Main function
    def run(self, run_id, src, dest, inputfile, algorithm, language):
        # TODO parameters are retrieved on kafka event
        # creating a folder with the id of the run
        try:
            os.mkdir("./{}".format(run_id))
        except Exception as e:
            logging.error("[ERROR] CREATING TMP FOLDER FAILED, DOCKER WONT ACCESS FILES!!! StackTrace: {}".format(e))
        # getting into this folder
        os.chdir("./{}".format(run_id))

        # here we create the code file and the data to be parsed, according to the languages we have
        self.create_files(src, inputfile, algorithm, language)

        # folder name after run id, we start docker from here

        image = 'urunner:python3.8'
        command = 'python3.8 code.py in.json'

        run_parameters = {'image': image,
                          'command': command}

        logging.info("new docker run into {}".format(os.getcwd()))

        # running docker with container Object (can attach)
        client = docker.client.from_env()
        container = client.containers.run(image=run_parameters['image'],
                                          command=run_parameters['command'],
                                          volumes={os.getcwd(): {'bind': '/code/', 'mode': 'rw'}},
                                          stderr=True, stdout=True, detach=True)

        logging.info("Running a new container ! ID: {}".format(container.id))

        # client.copy(container.id, "requirements.txt")
        container.wait()
        out = container.logs(stdout=True, stderr=False)
        err = container.logs(stdout=False, stderr=True)

        with open("out.json", "r") as file:
            artifact = file.read()
        response_for_backend = {'stdout': out,
                                'stderr': err,
                                'artifact': artifact}

        # running docker with low level API client (cannot attach)
        # configured_volumes = client.create_host_config(binds={run_folder: {'bind': '/code/', 'mode': 'rw'}})
        # container = client.create_container(image='urunner:python3.8', stdin_open=False, tty=False,
        #                                     command='ls 2> error 1> output', volumes=[run_folder],
        #                                     host_config=configured_volumes)
        # client.start(container)  # or client.start(container.get("Id")))

        self.clean_host_files(run_id=run_id)  # delete the run_id folder at the end of run

        logging.info(response_for_backend)
        logging.info("DOCKER ENDED")
        return {'lol': 'lel'}

    @staticmethod
    def clean_host_files(run_id):
        os.chdir("..")
        try:
            shutil.rmtree('./{}'.format(run_id), ignore_errors=False)
        except Exception as e:
            logging.error("clean_host_files: " + e)

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
        pass
        # server = ['localhost;9092']
        # producer = KafkaProducer(bootstrap_servers=[server], auto_offset_reset='earliest', enable_auto_commit=True,
        #                          value_serializer=lambda x: json.loads(x.decode('utf-8')))
        #
        # producer.send('urunner-ouput', results)
        # TODO produce to kafka topic

    # testings functions
    def test_run_python(self):
        last_data = kafka_mock()
        if last_data:
            self.run(last_data['id'], last_data['from'], last_data['to'],
                     last_data['inputfile'], last_data['algorithm'], last_data['language'])
        else:
            time.sleep(1)

