-----------------------------------------------------------------------------
|   dP     dP                                                               |
|   88     88                                                               |
|   88     88  88d888b.  dP    dP  88d888b.  88d888b.  .d8888b.  88d888b.   |
|   88     88  88'  `88  88    88  88'  `88  88'  `88  88ooood8  88'  `88   |
|   Y8.   .8P  88        88.  .88  88    88  88    88  88.  ...  88         |
|   `Y88888P'  dP        `88888P'  dP    dP  dP    dP  `88888P'  dP         |
-----------------------------------------------------------------------------

The Universal Runner is an attempt to run arbitrary code from any languages into standardised environments.

This is still a work in progress.

the runner can be deployed using three different methods:
    - [DONE] runner can be run locally for dev testing purpose, on a python virtual environment or local one
    - [DONE] And, so on, can be deployed on bare-metal instances
    - [WIP] or it also could be into a docker container

For all those deployments methods, the kafka configuration files located in urunner/config/kafka_config.py
    - We should have the possibility to use environment variables TODO
    - a small refactor of kafka configuration files for agent would be nice TODO

Supported Languages & And urunner steps
    Docker images:
        We have one image for each language supported by urunner:
         - python: urunner:python3.8 DONE
         - c:      urunner:c         TODO

    Runner steps:
    1) runner initialize, connect to the kafka queues INPUT and OUTPUT # DONE
        2) poll off the topic # DONE
            1 create a folder named by the run id, pour code and input file into it # DONE
            2 create run command by language used # DONE
            3 run docker container flagged with host files (code and data) as input # DONE
            4 docker container runs, creating output data and stdout stderr files into id folder # DONE
            5 runner assert parsed data and send back stdout & stderr to result message # DONE
    3) Produce data into output kafka topic # DONE


############ TO-DO LIST & SCRATCHES ################

###### AGENT ########
MULTITHREADING                                  TODO
TIMEOUT PROTECTION:                             DONE
STATS (timedelta / files sizes)                 DONE
COMPILED LANGUAGE:                              TODO
DEPLOYMENT                                      WIP
BETTER ERROR HANDLING                           DONE
E2E TESTING WITH EXTREME INPUTS                 DONE
CLEANING_AGENT TO REMOVE POTENTIALS LEFTOVERS   DONE
USING `--memory-reservation` on docker run      TODO

### DOCKER IMAGES ###
Languages:
Python                                          DONE
C                                               WIP
Js                                              TODO


(07/2021)