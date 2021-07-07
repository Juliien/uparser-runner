import logging
import os
import docker
import shutil

from urunner.tools import encode, decode
from urunner.kafka_wrapper import Producer

VALID_LANGUAGES = {'python': {'ext': '.py', 'image': 'urunner:python3.8', 'bin': 'python3'},
                   }  # insert new languages here

DUMMY_OUT_FILE_EXT = ".dummy"

class Run:
    _image = ""
    _command = ""
    _bin = ""
    _run_cmd = ""

    _client = None
    _container = None

    _input_less = False

    code_filename = ""
    in_filename = ""
    out_filename = ""

    code_ext = ""
    in_ext = ""
    out_ext = ""

    response = dict()
    error = ""

    Logger = None

    def __init__(self, run_id, src, dest, inputfile, algorithm, language, logger):
        if not src:
            self._input_less = True

        if not dest:
            self.out_ext = DUMMY_OUT_FILE_EXT

        self.run_id = run_id
        self.Logger = logger
        self.WrappedProducer = Producer()
        # SETUP: creating run id temporary folder, dive into it and prepare users files according to languages chosen
        self.create_run_folder_and_dive()
        self.setup_extensions(language, src, dest)
        self.prepare_files(in_encoded=inputfile, code_encoded=algorithm)
        # DOCKER: setup, create and log
        self.setup_docker()
        self.run_docker()
        self.retrieve_logs_and_artifact()
        # CLEANING
        self.send_response()
        self.clean_host_files()  # delete the run_id folder at the end of run

    def __del__(self):
        pass

    ### FILE SETUP ###
    def create_run_folder_and_dive(self):
        # creating a folder with the id of the run
        if not self.run_id:
            raise Exception("run id is NOT SET")
        try:
            os.mkdir(self.run_id)
        except Exception as e:
            self.Logger.error(e)

        try:
            os.chdir(self.run_id)
        except Exception as e:
            self.Logger.error(e)

        self.Logger.info("new docker run into {}".format(os.getcwd()))

    def setup_extensions(self, language, in_ext, out_ext):
        if language in VALID_LANGUAGES.keys():
            self.code_ext = VALID_LANGUAGES[language]['ext']
            self._image = VALID_LANGUAGES[language]['image']
            self._bin = VALID_LANGUAGES[language]['bin']
        else:
            raise Exception("INVALID CODE EXTENSION")

        self.in_ext = in_ext
        self.out_ext = out_ext

        self.code_filename = "code{}".format(self.code_ext)
        self.in_filename = "in.{}".format(self.in_ext)
        self.out_filename = "out.{}".format(self.out_ext)

    def prepare_files(self, in_encoded, code_encoded):
        # creating input file with right extension
        if not self._input_less:
            with open(self.in_filename, "w+") as in_file:
                in_file.write(decode(in_encoded).decode('utf-8'))

        # creating code file
        with open(self.code_filename, "w+") as code_file:
            code_file.write(decode(code_encoded).decode('utf-8'))

    ### DOCKER SETUP RUN AND RETRIEVING DATA
    def setup_docker(self):
        # run cmd formatting # TODO ERROR HANDLING
        self._run_cmd = "{} {} {}".format(self._bin, self.code_filename, self.in_filename)

        # running docker with container Object (can attach)
        self._client = docker.client.from_env()

    def run_docker(self):
        self._container = self._client.containers.run(image=self._image, command=self._run_cmd,
                                                      volumes={os.getcwd(): {'bind': '/code/', 'mode': 'rw'}},
                                                      stdout=True, stderr=True, detach=True)

        self.Logger.info("Running a new container ! ID: {}".format(self._container.id))
        self._container.wait()

    def retrieve_logs_and_artifact(self):
        # retrieving stderr and stdout
        out = self._container.logs(stdout=True, stderr=False).encode()
        err = self._container.logs(stdout=False, stderr=True).encode()

        try:
            with open(self.out_filename, "r") as file:
                artifact = file.read()
        except FileNotFoundError:
            artifact = None

        self.response = {'run_id': self.run_id, 'stdout': out, 'stderr': err, 'artifact': artifact}
        self.Logger.debug(self.response)

    ### KAFKA RESPONSE
    def send_response(self):
        self.WrappedProducer.producer.send('runner-output', str(self.response))

    def clean_host_files(self):
        os.chdir("..")
        try:
            shutil.rmtree(self.run_id, ignore_errors=False)
        except Exception as e:
            self.Logger.error("clean_host_files: {}".format(e))
