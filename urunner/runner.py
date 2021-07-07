import docker
import time
import sys
import os
import base64
import shutil
import logging

import signal
import sys

from kafka_wrapper import KafkaWrapper


def decode(to_decode):
    return base64.b64decode(to_decode)


def encode(to_encode):
    return base64.b64encode(to_encode)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Urunner(metaclass=Singleton):

    def __init__(self):
        # settings kafka wrapper
        self.kafka_wrapper = KafkaWrapper()

        signal.signal(signal.SIGINT, self.signal_handler)
        # init logs

        logging.basicConfig(filename='runner.log', stream=sys.stdout, filemode='w', level=logging.INFO)
        # root = logging.getLogger()
        # handler = logging.StreamHandler(sys.stdout)
        # handler.setLevel(logging.DEBUG)
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)
        # root.addHandler(handler)

        logging.info('test')
        # listening kafka input
        for k in self.kafka_wrapper.consumer:
            logging.info("adding values: {}".format(k.value))
            self.run(run_id=k.value['id'], src=k.value['from'], dest=k.value['to'], inputfile=k.value['inputfile'],
                     algorithm=k.value['algorithm'], language=k.value['language'])
            time.sleep(2)

    def __del__(self):
        print('Thanks for using Urunner ! :D')
        # self.end_time = datetime.datetime.utcnow()
        # logging.info("test ended: {}".format(datetime.datetime.utcnow()))
        #
        # self.run_time = self.end_time - self.start_time
        # logging.info("test tun time: {}".format(self.run_time))

    # Main function
    def run(self, run_id, src, dest, inputfile, algorithm, language):
        # creating a folder with the id of the run
        try:
            os.mkdir("./{}".format(run_id))
        except Exception as e:
            logging.warning(e)

        # getting into this folder
        os.chdir("./{}".format(run_id))

        # here we create the code file and the data to be parsed, according to the languages we have
        self.create_files(src, inputfile, algorithm, language)

        # folder name after run id, we start docker from here
        logging.info("new docker run into {}".format(os.getcwd()))

        # setting run parameters for docker
        image = 'urunner:python3.8'
        command = 'python3.8 code.py in.{}'.format(src)
        run_parameters = {'image': image, 'command': command}

        # running docker with container Object (can attach)
        client = docker.client.from_env()
        container = client.containers.run(image=run_parameters['image'], command=run_parameters['command'], stdout=True,
                                          volumes={os.getcwd(): {'bind': '/code/', 'mode': 'rw'}}, stderr=True, detach=True)
        logging.info("Running a new container ! ID: {}".format(container.id))
        container.wait()

        # retrieving stderr and stdout
        out = container.logs(stdout=True, stderr=False)
        err = container.logs(stdout=False, stderr=True)
        logging.info(type(out))
        logging.info(type(err))

        try:
            with open("out.{}".format(dest), "r") as file:
                artifact = file.read()
        except FileNotFoundError:
            artifact = "FILE NOT FOUND ERROR"

        response_for_backend = {'run_id': run_id, 'stdout': out, 'stderr': err, 'artifact': artifact}
        logging.info(response_for_backend)

        self.clean_host_files(run_id=run_id)  # delete the run_id folder at the end of run
        self.kafka_wrapper.producer.send('runner-output', str(response_for_backend))

    def signal_handler(self, sig, frame):
        logging.info(sig)
        logging.info(frame)
        self.kafka_wrapper.consumer.close()
        sys.exit(0)

    @staticmethod
    def clean_host_files(run_id):
        os.chdir("..")
        try:
            shutil.rmtree('./{}'.format(run_id), ignore_errors=False)
        except Exception as e:
            logging.error("clean_host_files: {}".format(e))

    @staticmethod
    def create_files(src, inputfile, algorithm, language):
        # creating input file with right extension
        with open("in.{}".format(src), "w+") as data_to_parse:
            data_to_parse.write(decode(inputfile).decode('utf-8'))

        # creating code files
        if language == "python":
            with open("code.py", "w+") as code_to_run:
                code_to_run.write(decode(algorithm).decode('utf-8'))
