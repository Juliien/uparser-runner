import docker
import time
import sys
import os
import shutil
import logging

from urunner.kafka_wrapper import Consumer
from urunner.run.Run import Run
from urunner.tools import decode, encode, kafka_mock


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Urunner(metaclass=Singleton):
    def __init__(self):
        # settings kafka wrapper
        self.WrappedConsumer = Consumer()

        # init logs

        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        root = logging.getLogger()
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

        # listening kafka input
        for k in self.WrappedConsumer.consumer:
            logging.info("adding values: {}".format(k.value))

            self.run = Run(run_id=k.value['id'], src=k.value['from'], dest=k.value['to'], inputfile=k.value['inputfile'],
                           algorithm=k.value['algorithm'], language=k.value['language'])

            time.sleep(2)

    def __del__(self):
        pass
        # self.end_time = datetime.datetime.utcnow()
        # logging.info("test ended: {}".format(datetime.datetime.utcnow()))
        #
        # self.run_time = self.end_time - self.start_time
        # logging.info("test tun time: {}".format(self.run_time))
