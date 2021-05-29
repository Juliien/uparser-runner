Runner steps:

1) docker start urunner
2) runner initialize, connect to the kafka queue
    2a) If queue is empty, passing back to idle mode
    2b) Else, Execute one poll off the topic
3) Code inspection, performance and all
4) Prepare code report
5) Send back data via API or Queue
6) All Done, try to poll next nor idle
