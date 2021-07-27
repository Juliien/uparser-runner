import datetime
import sys
import time

import logging
import os
import docker
import shutil

from tools import encode, decode
from kafka_wrapper import Producer


class Run:
    VALID_LANGUAGES = {'python': {'ext': '.py', 'image': 'urunner:python3.8', 'bin': 'python3', 'compiled': False},
                       'c': {'ext': '.c', 'image': 'urunner:c', 'bin': './a.out', 'compiler': 'gcc', 'compiled': True}
                       # insert new languages here
                       }

    DUMMY_OUT_FILE_EXT = ".dummy"
    TMP_RUN_DIR = "./tmp/"
    base_folder = ""

    _image = ""
    _command = ""
    _bin = ""
    _run_cmd = ""

    _client = None
    _container = None

    _input_less = False

    _start_time = None
    _end_time = None
    language = ""

    code_filename = ""
    in_filename = ""
    out_filename = ""

    code_ext = ""
    in_ext = ""
    out_ext = ""

    response = dict()
    error = ""

    Logger = None

    def __init__(self, run_id, src, dest, inputfile, algorithm, language):
        logging.info("------------------------------------ START RUN ------------------------------------")
        logging.info("run id: {}, src: {}, dest: {}, lang: {}".format(
            run_id, src, dest, language))

        # basic configuration
        if not src:
            self._input_less = True

        if not dest:
            self.out_ext = self.DUMMY_OUT_FILE_EXT

        self.run_id = run_id
        self.run_folder = self.run_id  # self.TMP_RUN_DIR +
        logging.info('workdir: {} run folder: {}'.format(os.getcwd(), self.run_folder))
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
        logging.info("------------------------------------- END RUN -------------------------------------")

    ### FILE SETUP ###
    def create_run_folder_and_dive(self):
        self.base_folder = os.getcwd()
        # creating a folder with the id of the run
        if not self.run_id:
            raise Exception("run id is NOT SET")
        try:
            os.mkdir(self.run_folder)
        except Exception as e:
            logging.error(e)

        try:
            os.chdir(self.run_folder)
        except Exception as e:
            logging.error(e)

    def setup_extensions(self, language, in_ext, out_ext):
        if language in self.VALID_LANGUAGES.keys():
            self.code_ext = self.VALID_LANGUAGES[language]['ext']
            self._image = self.VALID_LANGUAGES[language]['image']
            self._bin = self.VALID_LANGUAGES[language]['bin']
            self.language = language
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
        # run cmd formatting
        if self.VALID_LANGUAGES[self.language]['compiled']:
            self.build_compiled_image()
        else:
            self._run_cmd = "{} {} {}".format(self._bin, self.code_filename, self.in_filename)

        # running docker with container Object (can attach)
        self._client = docker.client.from_env()

    def build_compiled_image(self):
        print("compile here !")
        pass

    def run_docker(self):
        self._start_time = datetime.datetime.utcnow()
        self._container = self._client.containers.run(image=self._image, command=self._run_cmd,
                                                      volumes={self.run_folder: {'bind': '/code/', 'mode': 'rw'}},
                                                      stdout=True, stderr=True, detach=True)

        logging.info("Running a new container ! ID: {}".format(self._container.id))
        self._container.wait()
        self._end_time = datetime.datetime.utcnow()

    def retrieve_logs_and_artifact(self):
        # retrieving stderr and stdout
        out = self._container.logs(stdout=True, stderr=False).decode()
        err = self._container.logs(stdout=False, stderr=True).decode()

        try:
            with open(self.out_filename, "r") as file:
                artifact = file.read()
        except FileNotFoundError:
            artifact = None

        # out = encode(bytes(out, encoding='utf-8'))
        # err = encode(bytes(err, encoding='utf-8'))
        # artifact = encode(bytes(artifact, encoding='utf-8'))
        code_size = os.stat(self.run_folder + '/' + self.code_filename).st_size
        in_size, out_size = None, None
        if os.path.exists(self.run_folder + '/' + self.in_filename):
            in_size = os.stat(self.run_folder + '/' + self.in_filename).st_size

        if os.path.exists(self.run_folder + '/' + self.out_filename):
            out_size = os.stat(self.run_folder + '/' + self.out_filename).st_size

        stats = {'duration': self._end_time - self._start_time,
                 'code_size': code_size, 'in_size': in_size, 'out_size': out_size}

        logging.info(stats)
        self.response = {'run_id': self.run_id, 'stdout': out,
                         'stderr': err, 'artifact': artifact, 'stats': str(stats)}

        # logging.debug(self.response)

    ### KAFKA RESPONSE
    def send_response(self):
        self.WrappedProducer.producer.send('runner-output', self.response)

    def clean_host_files(self):
        logging.warning("cleaning files on host machine !")
        logging.warning(os.listdir(self.run_folder))
        os.chdir(self.base_folder)
        try:
            shutil.rmtree(self.run_folder, ignore_errors=True)
        except Exception as e:
            logging.error("clean_host_files: {}".format(e))

