import logging
import os
import docker
import shutil

from urunner.tools import encode, decode
from urunner.kafka_wrapper import Producer

VALID_LANGUAGES = { 'python':
                        {'ext': '.py',
                         'image': 'urunner:python3.8',
                         'bin': 'python3'}}


class Run:
    _image = ""
    _command = ""
    _bin = ""
    _run_cmd = ""

    _client = None
    _container = None

    code_filename = ""
    in_filename = ""
    out_filename = ""

    code_ext = ""
    in_ext = ""
    out_ext = ""

    response = dict()
    error = ""

    def __init__(self, run_id, src, dest, inputfile, algorithm, language):
        self.run_id = run_id

        self.WrappedProducer = Producer()
        # creating run id temporary folder, dive into it and prepare users files according to languages chosen
        self.create_run_folder_and_dive()
        self.setup_extensions(language, src, dest)
        self.prepare_files(in_encoded=inputfile, code_encoded=algorithm)

        # folder name after run id, we start docker from here, setting run parameters for docker
        self.clean_host_files()  # delete the run_id folder at the end of run

    def __del__(self):
        pass

    ### FILE SETUP ###
    def setup_extensions(self, language, in_ext, out_ext):
        if language in VALID_LANGUAGES.keys():
            self.code_ext = VALID_LANGUAGES[language]['ext']
            self._image = VALID_LANGUAGES[language]['image']
            self._bin = VALID_LANGUAGES[language]['bin']
        else:
            raise Exception("INVALID CODE EXTENSION")

        self.in_ext = in_ext
        self.out_ext = out_ext

        self.code_filename = "code.{}".format(self.code_ext)
        self.in_filename = "in.{}".format(self.in_ext)
        self.out_filename = "out.{}".format(self.out_ext)

    def prepare_files(self, in_encoded, code_encoded):
        # creating input file with right extension
        with open(self.in_ext, "w+") as in_file:
            in_file.write(decode(in_encoded).decode('utf-8'))

        # creating code file
        with open(self.code_filename, "w+") as code_file:
            code_file.write(decode(code_encoded).decode('utf-8'))

    def create_run_folder_and_dive(self):
        # creating a folder with the id of the run
        if not self.run_id:
            raise Exception("run id is NOT SET")
        try:
            os.mkdir("./{}".format(self.run_id))
        except Exception as e:
            logging.error(e)

        try:
            os.chdir(self.run_id)
        except Exception as e:
            logging.error(e)

        logging.info("new docker run into {}".format(os.getcwd()))
    ###

    def setup_docker(self):
        # run cmd formatting # TODO ERROR HANDLING
        self._run_cmd = "{} {} {}".format(self._bin, self.code_filename, self.in_filename)

        # running docker with container Object (can attach)
        self._client = docker.client.from_env()

    def run_docker(self):
        container = self._client.containers.run(image=self._image, command=self._run_cmd,
                                                volumes={os.getcwd(): {'bind': '/code/', 'mode': 'rw'}},
                                                stdout=True, stderr=True, detach=True)

        logging.info("Running a new container ! ID: {}".format(container.id))
        container.wait()
        self._container = container

    def retrieve_logs_and_artifact(self):
        # retrieving stderr and stdout
        out = self._container.logs(stdout=True, stderr=False)
        err = self._container.logs(stdout=False, stderr=True)

        try:
            with open("out.json", "r") as file:
                artifact = file.read().encode('utf-8')
        except FileNotFoundError:
            artifact = None

        NEW_KAFKA_MESSAGE = {'run_id': self.run_id, 'stdout': out, 'stderr': err, 'artifact': artifact}
        logging.debug(NEW_KAFKA_MESSAGE)

        self.producer.send('runner-output', NEW_KAFKA_MESSAGE)

    ##########
    def clean_host_files(self):
        os.chdir("..")
        try:
            shutil.rmtree(self.run_id, ignore_errors=False)
        except Exception as e:
            logging.error("clean_host_files: {}".format(e))
