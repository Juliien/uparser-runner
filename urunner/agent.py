import os
import time
import logging

import requests.exceptions

from kafka_wrapper import Consumer
from run.Run import Run
import sys


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Urunner(metaclass=Singleton):
    Logger = None

    def __init__(self):
        self.parametrize_logging()

        # settings kafka wrapper
        self.WrappedConsumer = Consumer()  # logger=self.Logger)

        # if not os.path.exists("./tmp/"):
        #     os.mkdir("./tmp/")
        # listening kafka input
        try:
            for k in self.WrappedConsumer.consumer:
                self.run = Run(run_id=k.value['id'], src=k.value['from'], dest=k.value['to'], inputfile=k.value['inputfile'],
                               algorithm=k.value['algorithm'], language=k.value['language'])
                del self.run
                time.sleep(1)
        except KeyboardInterrupt:
            logging.warning("Keyboard Interrupt !")

    @staticmethod
    def parametrize_logging():
        log_format = '\033[95m[%(levelname)-8s][%(asctime)s][%(filename)s][%(funcName)s][%(lineno)s]:\033[0m %(name)s : %(message)s'
        logging.basicConfig(datefmt='%H:%M:%S', level=logging.DEBUG,   format=log_format, stream=sys.stdout)
        logging.info('Urunner Logging Initialization')

    def __del__(self):
        logging.info('Thanks for using Urunner ! :D')
