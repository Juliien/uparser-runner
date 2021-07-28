from urunner.kafka_wrapper import Producer
import pytest

INPUT_TOPIC = "runner-input"


@pytest.fixture
def prod():
    return Producer()


@pytest.mark.skip("")
def test_python_hello_world(prod):
    test_hello_world = {'id': '1234', 'from': 'json', 'to': 'csv', 'inputfile': 'eyAnaGVsbG8nOiAnd29ybGQnfQ==',
                        'algorithm': 'cHJpbnQoImhlbGxvIHdvcmxkISIp', 'language': 'python'}

    prod.producer.send(INPUT_TOPIC, test_hello_world).get()


@pytest.mark.skip("")
def test_python_file(prod):
    tmp_algo = "d2l0aCBvcGVuKCJvdXQuanNvbiIsICJ3KyIpIGFzIGZpbGU6CiAgICBmaWxlLndyaXRlKCJEVU1NWSBGSUxFIEZPUiBGSUxFIFJFVFJJRVZFIFRFU1QiKQo= "

    test_file_generation = {'id': '666', 'from': 'csv', 'to': 'json', 'inputfile': 'eyAnaGVsbG8nOiAnd29ybGQnfQ==',
                            'algorithm': tmp_algo, 'language': 'python'}

    prod.producer.send(INPUT_TOPIC, test_file_generation).get()


@pytest.mark.skip("")
def test_python_e2e(prod):
    test_real = {'id': '2838f3e8-61e7-49a0-84dc-7f2892193ff8',
                 'inputfile': 'bm9tDQpkYSBjb3J0ZQ0KZHVwb250DQpkdXByZXQNCg==',
                 'from': 'csv', 'to': 'json',
                 'algorithm': 'aW1wb3J0IHN5cwppbXBvcnQganNvbgppbXBvcnQgY3N2Cgpqc29uQXJyYXkgPSBbXQp3aXRoIG9wZW4oc3lzLmFyZ3ZbMV0pIGFzIGZpbGU6CiAgICBjc3ZSZWFkZXIgPSBjc3YuRGljdFJlYWRlcihmaWxlKQogICAgZm9yIHJvdyBpbiBjc3ZSZWFkZXI6CiAgICAgICAganNvbkFycmF5LmFwcGVuZChyb3cpCiAKd2l0aCBvcGVuKCJvdXQuanNvbiIsICd3KycsIGVuY29kaW5nPSd1dGYtOCcpIGFzIGpzb25GaWxlOgogICAganNvblN0cmluZyA9IGpzb24uZHVtcHMoanNvbkFycmF5LCBpbmRlbnQ9NCkKICAgIGpzb25GaWxlLndyaXRlKGpzb25TdHJpbmcp',
                 'language': 'python'}

    prod.producer.send(INPUT_TOPIC, test_real).get()


@pytest.mark.skip("json to csv")
def test_json_to_csv(prod):
    test_csv = {"id": "1",
                "inputfile": "ew0KICAgICJlbWFpbCI6ICJqdWxpZW5AZ21haWwuY29tIiwNCiAgICAicGFzc3dvcmQiOiAidGVzdCIsDQogICAgIm5hbWUiOiAidG90byIsDQogICAgImFtZGluIjogdHJ1ZQ0KfQ==",
                "algorithm": "aW1wb3J0IGpzb24NCmltcG9ydCBjc3YNCmltcG9ydCBzeXMNCiANCndpdGggb3BlbihzeXMuYXJndlsxXSkgYXMganNvbl9maWxlOg0KICAgIGpzb25fZGF0YSA9IGpzb24ubG9hZChqc29uX2ZpbGUpDQoNCndpdGggb3Blbignb3V0LmNzdicsICdhJykgYXMgZl9vYmplY3Q6DQogICAgZHcgPSBjc3YuRGljdFdyaXRlcihmX29iamVjdCwgZGVsaW1pdGVyPSc7JywgZmllbGRuYW1lcz1qc29uX2RhdGEua2V5cygpKQ0KICAgIGR3LndyaXRlaGVhZGVyKCkNCiAgICBkdy53cml0ZXJvdyhqc29uX2RhdGEpDQogICANCg==",
                "from": "json", "to": "csv", "language": "python"}

    prod.producer.send(INPUT_TOPIC, test_csv).get()


#@pytest.mark.skip("infinite loop")
def test_timeout_protection(prod):
    test_timeout = {"id": "1", "inputfile": "",
                    "algorithm": "aW1wb3J0IHRpbWUKCndoaWxlIDE6CiAgICBwcmludCgibG9sIikKICAgIHRpbWUuc2xlZXAoMSkg",
                    "from": "", "to": "", "language": "python"}

    prod.producer.send(INPUT_TOPIC, test_timeout).get()
