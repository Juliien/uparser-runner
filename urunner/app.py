from runner import Urunner
from kafka_wrapper import KafkaWrapper

if __name__ == "__main__":
    # urunner = Urunner()
    # urunner.test_run_python()  # IS ONLY HERE TO HELP DEV WITHOUT KAFKA TOPIC CONNECTED
    wrapper = KafkaWrapper()
    # for message in wrapper.consumer:
    #     print(message.value)
