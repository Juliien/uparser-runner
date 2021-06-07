Runner steps:

runner can be run locally for dev testing purpose,
deployed to a cloud instance,
or it also could be into a docker container # TODO

1) runner initialize, connect to the kafka queue
    2a) If queue is empty, it idle of 1s
    2b) Else, Execute one poll off the topic
        1 create a folder named by the run id, pour code and input file into it
        2 create run command by language used
        3 run docker container flagged with host files (code and data) as input
        4 docker container runs, creating output data and stdout stderr files into id folder
        5 runner assert parsed data and send back stdout & stderr to result message
3) Produce data into output kafka topic
4) Repeat
