
- runner can be run locally for dev testing purpose,
- deployed to a cloud instance,
- or it also could be into a docker container # TODO

to start urunner: python3.8 app.py
Docker images:
We have one image for each language possible, urunner:python3.8 for example
# TODO define run command for compiled languages



Runner steps:
1) runner initialize, connect to the kafka queues INPUT and OUTPUT # TODO
    2) poll off the topic # TODO
        1 create a folder named by the run id, pour code and input file into it # DONE
        2 create run command by language used # DONE
        3 run docker container flagged with host files (code and data) as input # DONE
        4 docker container runs, creating output data and stdout stderr files into id folder # DONE
        5 runner assert parsed data and send back stdout & stderr to result message # TODO NEXT STEP
3) Produce data into output kafka topic # TODO


flags dockers we should be using # TODO
--memory-reservation