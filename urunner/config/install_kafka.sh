mkdir tmp-kafka-install
cd tmp-kafka-install
sudo apt install -y default-jdk
wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
tar xzf kafka_2.13-2.7.0.tgz
mv kafka_2.13-2.7.0 /usr/local/kafka
cd ..
rm -rf './kafka_2.13-2.7.0'

# for the next two cp we may use links to directly refer to those files
cp zookeeper.service /etc/systemd/system/zookeeper.service
cp kafka.service /etc/systemd/system/kafka.service

systemctl daemon-reload
sudo systemctl start zookeeper
sudo systemctl start kafka
sudo systemctl status kafka

/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic runner-input
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic runner-output
