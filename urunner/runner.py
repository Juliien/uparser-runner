import time
import logging

from urunner.kafka_wrapper import Consumer
from urunner.run.Run import Run
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

        # listening kafka input
        for k in self.WrappedConsumer.consumer:
            self.Logger.info("adding values: {}".format(k.value))

            self.run = Run(run_id=k.value['id'], src=k.value['from'], dest=k.value['to'], inputfile=k.value['inputfile'],
                           algorithm=k.value['algorithm'], language=k.value['language'], logger=self.Logger)
            time.sleep(2)

    def parametrize_logging(self):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        self.Logger = logging.getLogger(__name__)
        self.Logger.info('Urunner Logging Initialization')
        self.Logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        handler = logging.StreamHandler(sys.stdout)

        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)

        self.Logger.addHandler(handler)

    def __del__(self):
        print('Thanks for using Urunner ! :D')
        # self.end_time = datetime.datetime.utcnow()
        # logging.info("test ended: {}".format(datetime.datetime.utcnow()))
        #
        # self.run_time = self.end_time - self.start_time
        # logging.info("test tun time: {}".format(self.run_time))
