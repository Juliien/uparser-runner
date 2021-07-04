cfg = {'input': {'topic': 'runner-input',
                 'server': "localhost:9092"},
       'output': {'topic': 'runner-output',
                  'server': 'localhost:9092'}}

"/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic runner-output"
"/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic runner-input"
