from urunner.kafka_wrapper import Producer
import pytest

INPUT_TOPIC = "runner-input"


@pytest.fixture
def prod():
    return Producer()


def test_c_lang(prod):
    test_real = {'id': '2838f3e8-61e7-49a0-84dc-7f2892193ff8',
                 'inputfile': 'bm9tDQpkYSBjb3J0ZQ0KZHVwb250DQpkdXByZXQNCg==',
                 'from': 'csv', 'to': 'json',
                 'algorithm': 'aW1wb3J0IHN5cwppbXBvcnQganNvbgppbXBvcnQgY3N2Cgpqc29uQXJyYXkgPSBbXQp3aXRoIG9wZW4oc3lzLmFyZ3ZbMV0pIGFzIGZpbGU6CiAgICBjc3ZSZWFkZXIgPSBjc3YuRGljdFJlYWRlcihmaWxlKQogICAgZm9yIHJvdyBpbiBjc3ZSZWFkZXI6CiAgICAgICAganNvbkFycmF5LmFwcGVuZChyb3cpCiAKd2l0aCBvcGVuKCJvdXQuanNvbiIsICd3KycsIGVuY29kaW5nPSd1dGYtOCcpIGFzIGpzb25GaWxlOgogICAganNvblN0cmluZyA9IGpzb24uZHVtcHMoanNvbkFycmF5LCBpbmRlbnQ9NCkKICAgIGpzb25GaWxlLndyaXRlKGpzb25TdHJpbmcp',
                 'language': 'c'}

    prod.producer.send(INPUT_TOPIC, test_real).get()


