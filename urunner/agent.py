import os
import time
import logging

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

        os.mkdir("./tmp/")
        # listening kafka input
        try:
            for k in self.WrappedConsumer.consumer:
                self.run = Run(run_id=k.value['id'], src=k.value['from'], dest=k.value['to'], inputfile=k.value['inputfile'],
                               algorithm=k.value['algorithm'], language=k.value['language'])
                time.sleep(2)
        except KeyboardInterrupt:
            logging.warning("Keyboard Interrupt !")

    @staticmethod
    def parametrize_logging():
        log_format = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'

        logging.basicConfig(datefmt='%m/%d/%Y, %H:%M:%S', level=logging.DEBUG,   format=log_format, stream=sys.stdout)
        logging.info('Urunner Logging Initialization')

    def __del__(self):
        logging.info('Thanks for using Urunner ! :D')
