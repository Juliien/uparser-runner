from urunner.kafka_wrapper import Producer


def kafka_mock():
    test_hello_world = {'id': '1234', 'from': 'json', 'to': 'csv', 'inputfile': 'eyAnaGVsbG8nOiAnd29ybGQnfQ==',
                        'algorithm': 'cHJpbnQoImhlbGxvIHdvcmxkISIp', 'language': 'python'}

    tmp_algo = "d2l0aCBvcGVuKCJvdXQuanNvbiIsICJ3KyIpIGFzIGZpbGU6CiAgICBmaWxlLndyaXRlKCJEVU1NWSBGSUxFIEZPUiBGSUxFIFJFVFJJRVZFIFRFU1QiKQo= "

    test_file_generation = {'id': '666', 'from': 'csv', 'to': 'json', 'inputfile': 'eyAnaGVsbG8nOiAnd29ybGQnfQ==',
                            'algorithm': tmp_algo, 'language': 'python'}

    test = [test_hello_world, test_file_generation]
    return test[0]


if __name__ == "__main__":
    producer = Producer()
    data = kafka_mock()
    producer.producer.send("runner-input", data).get()
    print("integration test end")

