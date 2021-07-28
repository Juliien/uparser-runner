import datetime
import logging
import os
import shutil
import signal

import docker

from kafka_wrapper import Producer
from tools import decode


# TIMEOUT PROTECTION

def log_color(string):
    logging.info('\033[96m' + str(string) + '\033[0m')


class TimeOutException(Exception):
    pass


def alarm_handler(signum, frame):
    log_color("RUN TIMEOUTED ! HARAKIRI!")
    raise TimeOutException()


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
    timeout = False

    def __init__(self, run_id, src, dest, inputfile, algorithm, language):
        log_color("------------------------------------ START RUN {} ------------------------------------".format(run_id))
        log_color("run id: {}, src: {}, dest: {}, lang: {}".format(
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

        try:
            signal.signal(signal.SIGALRM, alarm_handler)
            signal.alarm(8)
            self.run_docker()
            signal.alarm(0)
            self.retrieve_logs_and_artifact()
        except TimeOutException as e:
            Run.unexpected_error_response(self.run_id, e)

        self.send_response()
        self.clean_host_files()  # delete the run_id folder at the end of run
        log_color("------------------------------------- END RUN {} -------------------------------------".format(self.run_id))

    # BUILDING KAFKA RESPONSE AND REPONSE ERROR PRESET
    @staticmethod
    def build_response(run_id, stdout, stderr, artifact, stats):
        response = {'run_id': run_id,
                    'stdout': stdout,
                    'stderr': stderr,
                    'artifact': artifact,
                    'stats': stats}

        logging.info("{} response : {}".format(run_id, response))
        return response

    @staticmethod
    def unexpected_error_response(run_id, error_msg):
        logging.error(error_msg)
        prod = Producer()
        response = Run.build_response(run_id=run_id, stdout="UNEXPECTED ERROR\n", stderr="UNEXPECTED ERROR\n",
                                      artifact=None, stats=None)
        prod.producer.send('runner-output', response)

    ### FILE SETUP ###
    def create_run_folder_and_dive(self):
        # creating a folder with the id of the run
        if not self.run_id:
            raise Exception("run id is NOT SET")
        if os.path.exists(self.run_folder):
            shutil.rmtree(self.run_folder, ignore_errors=True)
        else:
            os.mkdir(self.run_folder)

        # try:
        #     os.chdir(self.run_folder)
        # except Exception as e:
        #     logging.error(e)

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
        log_color(os.listdir('.'))
        if not self._input_less:
            with open(os.path.join(self.run_folder, self.in_filename), "w+") as in_file:
                in_file.write(decode(in_encoded).decode('utf-8'))

        # creating code file
        with open(os.path.join(self.run_folder, self.code_filename), "w+") as code_file:
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
        logging.info("docker workdir: {}".format(os.getcwd()))
        logging.info("docker run dir content: {}".format(os.listdir(os.path.join(os.getcwd(), self.run_folder))))

        self._container = self._client.containers.run(image=self._image, command=self._run_cmd,
                                                      volumes={os.path.join(os.getcwd(), self.run_folder): {'bind': '/code/', 'mode': 'rw'}},
                                                      stdout=True, stderr=True, detach=True, )

        log_color("Running a new container ! ID: {}".format(self._container.id))
        self._container.wait()
        self._end_time = datetime.datetime.utcnow()

    def retrieve_logs_and_artifact(self):
        # retrieving stderr and stdout

        logging.info(os.getcwd())
        os.chdir(self.run_folder)
        out = self._container.logs(stdout=True, stderr=False).decode()
        err = self._container.logs(stdout=False, stderr=True).decode()

        artifact = None
        if os.path.exists(self.out_filename):
            with open(self.out_filename, "r") as file:
                artifact = file.read()

        # out = encode(bytes(out, encoding='utf-8'))
        # err = encode(bytes(err, encoding='utf-8'))
        # artifact = encode(bytes(artifact, encoding='utf-8'))

        in_size, out_size = 0, 0
        code_size = os.stat(self.code_filename).st_size

        if os.path.exists(self.in_filename):
            in_size = os.stat(self.in_filename).st_size

        if os.path.exists(self.out_filename):
            out_size = os.stat(self.out_filename).st_size

        timedelta = self._end_time - self._start_time

        stats = {'duration': str(timedelta),
                 'code_size': code_size, 'in_size': in_size, 'out_size': out_size}
        logging.info(stats)

        self.response = Run.build_response(run_id=self.run_id, stdout=out, stderr=err, artifact=artifact, stats=stats)
        os.chdir('..')

    ### KAFKA RESPONSE
    def send_response(self):
        self.WrappedProducer.producer.send('runner-output', self.response)

    def clean_host_files(self):
        logging.info("DELETING HOST MACHINE FILES")
        shutil.rmtree(self.run_folder, ignore_errors=True)
        assert self.run_id not in os.listdir('.'), "Left over folder in URUNNER !!!"
