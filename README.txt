-----------------------------------------------------------------------------
|   dP     dP                                                               |
|   88     88                                                               |
|   88     88  88d888b.  dP    dP  88d888b.  88d888b.  .d8888b.  88d888b.   |
|   88     88  88'  `88  88    88  88'  `88  88'  `88  88ooood8  88'  `88   |
|   Y8.   .8P  88        88.  .88  88    88  88    88  88.  ...  88         |
|   `Y88888P'  dP        `88888P'  dP    dP  dP    dP  `88888P'  dP         |
-----------------------------------------------------------------------------

The Universal Runner is an attempt to run arbitrary code from any languages into standardised environments.

This is a work in progress. (07/2021)

- runner can be run locally for dev testing purpose,
- deployed to a cloud instance,
- or it also could be into a docker container # TODO

to start urunner: python3.8 app.py
Docker images:
We have one image for each language possible, urunner:python3.8 for example
# TODO define run command for compiled languages

Runner steps:
1) runner initialize, connect to the kafka queues INPUT and OUTPUT # DONE
    2) poll off the topic # DONE
        1 create a folder named by the run id, pour code and input file into it # DONE
        2 create run command by language used # DONE
        3 run docker container flagged with host files (code and data) as input # DONE
        4 docker container runs, creating output data and stdout stderr files into id folder # DONE
        5 runner assert parsed data and send back stdout & stderr to result message # DONE
3) Produce data into output kafka topic # DONE

flags dockers we should be using # TODO
--memory-reservation