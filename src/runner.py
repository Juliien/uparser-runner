from src.user_code.uparser import run
from src.kafka_wrapper import KafkaWrapper

from src.errors.extention_error import ExtensionError
import datetime
import logging
import sys

# ENV Values

RESSOURCES_DIR = "ressources/"
GENERATED_BY_USER_DIR = RESSOURCES_DIR + "generated_by_user/"
DESTINATION_PATHNAME_FORMAT = GENERATED_BY_USER_DIR + "{}"
MOCK_DIR = RESSOURCES_DIR + "mock_parsing_data/"
MOCK_JSON = "MOCK_DATA.json"
DESTINATION_NAME = ""

VALID_EXTENSION = ["csv", "json"]


class Urunner:
    def __init__(self):
        # settings internals values
        self.dest_name = ""
        self.source_name = ""
        self.start_time = datetime.datetime.utcnow()

        # init logs
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        logging.info("test started: {}".format(datetime.datetime.utcnow()))
        logging.info("Parsing {} to this extenstion: ".format(MOCK_JSON))

        # connecting to kafka
        self.KafkaWrapper = KafkaWrapper() # default wrapper

        #
        self.create_dest_name_from_source(MOCK_JSON, ".csv")
        self.create_ressource_path()
        self.check_parser_syntax()

        run(source_pathname=self.source_name, destination_pathname=self.dest_name)

    def __del__(self):
        self.end_time = datetime.datetime.utcnow()
        logging.info("test ended: {}".format(datetime.datetime.utcnow()))

        self.run_time = self.end_time - self.start_time
        logging.info("test tun time: {}".format(self.run_time))

    @staticmethod
    def check_parser_syntax():
        pass

    # TODO create destination and source full path to runner
    def create_ressource_path(self):
        pass

    def idle(self):
        pass

    def run(self):
        pass

    def run_docker(self):


    # check syntax and extension of source and destination file
    def create_dest_name_from_source(self, source_filename: str, extension: str):
        self.source_name = source_filename
        split = source_filename.split('.')
        file_name = split[0]
        extention = split[1]
        if extention not in VALID_EXTENSION:
            raise Exception
        self.dest_name = file_name + extension