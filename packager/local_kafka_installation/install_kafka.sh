mkdir tmp-kafka-install
cd tmp-kafka-install
sudo apt install -y default-jdk
wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
tar xzf kafka_2.13-2.8.0.tgz
sudo mv kafka_2.13-2.8.0 /usr/local/kafka
cd ..
rm -rf './tmp-kafka-install'

# for the next two cp we may use links to directly refer to those files
sudo cp zookeeper.service /etc/systemd/system/zookeeper.service
sudo cp kafka.service /etc/systemd/system/kafka.service

systemctl daemon-reload
sudo systemctl start zookeeper
sudo systemctl start kafka
sudo systemctl status kafka

sleep 2

/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic runner-input
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic runner-output
