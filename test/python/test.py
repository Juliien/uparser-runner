from urunner.kafka_wrapper import Producer
import pytest

INPUT_TOPIC = "runner-input"


@pytest.fixture
def prod():
    return Producer()


def test_python_hello_world(prod):
    test_hello_world = {'id': '1234', 'from': 'json', 'to': 'csv', 'inputfile': 'eyAnaGVsbG8nOiAnd29ybGQnfQ==',
                        'algorithm': 'cHJpbnQoImhlbGxvIHdvcmxkISIp', 'language': 'python'}

    prod.producer.send(INPUT_TOPIC, test_hello_world).get()


def test_python_file(prod):
    tmp_algo = "d2l0aCBvcGVuKCJvdXQuanNvbiIsICJ3KyIpIGFzIGZpbGU6CiAgICBmaWxlLndyaXRlKCJEVU1NWSBGSUxFIEZPUiBGSUxFIFJFVFJJRVZFIFRFU1QiKQo= "

    test_file_generation = {'id': '666', 'from': 'csv', 'to': 'json', 'inputfile': 'eyAnaGVsbG8nOiAnd29ybGQnfQ==',
                            'algorithm': tmp_algo, 'language': 'python'}

    prod.producer.send(INPUT_TOPIC, test_file_generation).get()


def test_python_e2e(prod):
    test_real = {'id': '2838f3e8-61e7-49a0-84dc-7f2892193ff8',
                 'inputfile': 'bm9tDQpkYSBjb3J0ZQ0KZHVwb250DQpkdXByZXQNCg==',
                 'from': 'csv', 'to': 'json',
                 'algorithm': 'aW1wb3J0IHN5cwppbXBvcnQganNvbgppbXBvcnQgY3N2Cgpqc29uQXJyYXkgPSBbXQp3aXRoIG9wZW4oc3lzLmFyZ3ZbMV0pIGFzIGZpbGU6CiAgICBjc3ZSZWFkZXIgPSBjc3YuRGljdFJlYWRlcihmaWxlKQogICAgZm9yIHJvdyBpbiBjc3ZSZWFkZXI6CiAgICAgICAganNvbkFycmF5LmFwcGVuZChyb3cpCiAKd2l0aCBvcGVuKCJvdXQuanNvbiIsICd3KycsIGVuY29kaW5nPSd1dGYtOCcpIGFzIGpzb25GaWxlOgogICAganNvblN0cmluZyA9IGpzb24uZHVtcHMoanNvbkFycmF5LCBpbmRlbnQ9NCkKICAgIGpzb25GaWxlLndyaXRlKGpzb25TdHJpbmcp',
                 'language': 'python'}

    prod.producer.send(INPUT_TOPIC, test_real).get()


if __name__ == '__main__':
    test_python_e2e(prod())
