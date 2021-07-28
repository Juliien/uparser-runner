import datetime
import logging
import os
import shutil
import signal

import docker

from kafka_wrapper import Producer
from tools import decode


def log_cyan(string):
    logging.info('\033[96m' + str(string) + '\033[0m')


def log_red(string):
    logging.info('\033[91m' + str(string) + '\033[0m')


# TIMEOUT PROTECTION
class TimeOutException(Exception):
    pass


TIMEOUT = False


def alarm_handler(signum, frame):
    log_cyan("RUN TIMEOUTED ! HARAKIRI!")
    TIMEOUT = True
    raise TimeOutException()


class Run:
    VALID_LANGUAGES = {'python': {'ext': '.py', 'image': 'urunner:python3.8', 'bin': 'python3', 'compiled': False},
                       'c': {'ext': '.c', 'image': 'urunner:c', 'bin': './a.out', 'compiler': 'gcc', 'compiled': True}
                       # insert new languages here
                       }

    DUMMY_OUT_FILE_EXT = ".dummy"
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

    error = ""
    timeout = False

    def __init__(self, run_id, src, dest, inputfile, algorithm, language):
        log_cyan("------------------------------------ START RUN {} ------------------------------------".format(run_id))
        log_cyan("run id: {}, src: {}, dest: {}, lang: {}".format(
            run_id, src, dest, language))

        # basic configuration
        if not src:
            self._input_less = True

        if not dest:
            self.out_ext = self.DUMMY_OUT_FILE_EXT

        self.response = Run.build_response(run_id=run_id, stdout="urunner: RESPONSE NOT CREATED ERROR\n",
                                           stderr="urunner: RESPONSE NOT CREATED ERROR\n",
                                           artifact=None, stats=None)
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

        try:
            signal.signal(signal.SIGALRM, alarm_handler)
            signal.alarm(10)
            self.run_docker()
            signal.alarm(0)
            # run is ok, we build response from local files
            if not TIMEOUT:
                self.response = self.retrieve_logs_and_artifact()

        except TimeOutException as e:
            logging.error(e)
            # run is KO, we build dummy response with error
            self.response = Run.build_response(run_id=self.run_id, stdout="urunner: TIMEOUT ERROR\n",
                                               stderr="urunner: TIMEOUT ERROR\n",
                                               artifact=None, stats=None)

        log_red("Run ID: {} ENDED! Response: {}".format(self.run_id, self.response))

    def __del__(self):
        self.send_response()  # anyways, send the response back to kafka
        self.clean_host_files()  # delete the run_id folder at the end of run
        log_cyan("------------------------------------- END RUN {} -------------------------------------".format(self.run_id))

    # BUILDING KAFKA RESPONSE AND RESPONSE ERROR PRESET
    @staticmethod
    def build_response(run_id, stdout, stderr, artifact, stats):
        response = {'run_id': run_id,
                    'stdout': stdout,
                    'stderr': stderr,
                    'artifact': artifact,
                    'stats': stats}

        return response

    ### FILE SETUP ###
    def create_run_folder_and_dive(self):
        # creating a folder with the id of the run
        if not self.run_id:
            raise Exception("run id is NOT SET")
        # if same run id leftover folder is present, just delete it completely and recreate it
        if os.path.exists(self.run_folder):
            shutil.rmtree(self.run_folder, ignore_errors=True)
        os.mkdir(self.run_folder)

    def setup_extensions(self, language, in_ext, out_ext):
        # creating files names with corresponding extension
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

    def prepare_files(self, code_encoded, in_encoded=""):
        # creating input file with right extension
        log_cyan(os.listdir('.'))
        if not self._input_less:
            with open(os.path.join(self.run_folder, self.in_filename), "a+") as in_file:
                in_file.write(decode(in_encoded).decode('utf-8'))

        # creating code file
        with open(os.path.join(self.run_folder, self.code_filename), "a+") as code_file:
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

    @staticmethod
    def build_compiled_image():
        pass

    def run_docker(self):
        # running docker, getting start time and end time, and waiting for completion
        self._start_time = datetime.datetime.utcnow()

        logging.info("docker run dir content: {}".format(os.listdir(os.path.join(os.getcwd(), self.run_folder))))

        log_cyan(os.getcwd())
        docker_shared_folder = os.path.join(os.getcwd(), self.run_folder)
        logging.info(docker_shared_folder)
        self._container = self._client.containers.run(volumes={docker_shared_folder: {'bind': '/code/', 'mode': 'rw'}},
                                                      image=self._image, command=self._run_cmd,
                                                      stdout=True, stderr=True, detach=True)
        log_cyan("Running a new container ! ID: {}".format(self._container.id))
        self._container.wait()
        self._end_time = datetime.datetime.utcnow()

    def retrieve_logs_and_artifact(self):
        # retrieving stderr and stdout
        logging.info(os.getcwd())
        os.chdir(self.run_folder)
        out = self._container.logs(stdout=True, stderr=False).decode()
        err = self._container.logs(stdout=False, stderr=True).decode()

        # retrieve artifact file generated
        artifact = None
        if os.path.exists(self.out_filename):
            with open(self.out_filename, "r") as file:
                artifact = file.read()

        # size stats gathering
        in_size, out_size = 0, 0
        code_size = os.stat(self.code_filename).st_size

        if os.path.exists(self.in_filename):
            in_size = os.stat(self.in_filename).st_size

        if os.path.exists(self.out_filename):
            out_size = os.stat(self.out_filename).st_size

        # calculating runtime
        timedelta = self._end_time - self._start_time

        # compiling stats
        stats = {'duration': str(timedelta), 'code_size': code_size, 'in_size': in_size, 'out_size': out_size}
        os.chdir('..')
        return Run.build_response(run_id=self.run_id, stdout=out, stderr=err, artifact=artifact, stats=stats)

    ### KAFKA RESPONSE
    def send_response(self):
        self.WrappedProducer.producer.send('runner-output', self.response)

    def clean_host_files(self):
        logging.info('rm {}'.format(self.run_folder))
        shutil.rmtree(self.run_folder, ignore_errors=True)
        assert self.run_id not in os.listdir('.'), "Left over folder in URUNNER {}!!!.".format(self.run_id)
