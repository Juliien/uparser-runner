from src.user_code.uparser import run
import datetime
import logging
import sys


class Urunner:
    def __init__(self):
        self.start_time = datetime.datetime.utcnow()
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        logging.info("test started: {}".format(datetime.datetime.utcnow()))
        self.check_parser_syntax()

    def __del__(self):
        self.end_time = datetime.datetime.utcnow()
        logging.info("test ended: {}".format(datetime.datetime.utcnow()))

        self.run_time = self.end_time - self.start_time
        logging.info("test tun time: {}".format(self.run_time))

    @staticmethod
    def check_parser_syntax():
        print("running uparser: {}".format(run()))
