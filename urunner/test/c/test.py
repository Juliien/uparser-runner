from urunner.kafka_wrapper import Producer
import pytest

INPUT_TOPIC = "runner-input"


@pytest.fixture
def prod():
    return Producer()


@pytest.mark.skip("errored")
def test_c_lang_errored(prod):
    test_real = {'id': '2838f3e8-61e7-49a0-84dc-7f2892193ff8',
                 'inputfile': 'bm9tDQpkYSBjb3J0ZQ0KZHVwb250DQpkdXByZXQNCg==',
                 'from': 'csv', 'to': 'json',
                 'algorithm': 'I2luY2x1ZGUJPHN0ZGlvLmg+DQogaW50CQltYWluKGludCBhYywgY2hhciAqKmF2KQ0Kew0KICBpbnQJCWk7DQogIEZJTEUJCSpmcHRyOw0KICBjaGFyCQlmbls1MF07DQogIGNoYXIJCXN0cltdID0gInJ1bm5lciBSb2Nrc1xuIjsNCiAgDQogIGZwdHIgPSBmb3BlbigiZnB1dGNfdGVzdC5qc29uIiwgInciKTsNCiAgDQogIGZvciAoaSA9IDA7IHN0cltpXSAhPSAnXG4nOyBpKyspDQogICAgZnB1dGMoc3RyW2ldLCBmcHRyKTsNCiAgDQogIGZjbG9zZShmcHRyKTtYDQogIHJldHVybiAwOw0KfQ==',
                 'language': 'c'}

    prod.producer.send(INPUT_TOPIC, test_real).get()


def test_c_lang_valid(prod):
    test_real = {'id': '2838f3e8-61e7-49a0-84dc-7f2892193ff8',
                 'inputfile': 'bm9tDQpkYSBjb3J0ZQ0KZHVwb250DQpkdXByZXQNCg==',
                 'from': 'csv', 'to': 'json',
                 'algorithm': 'I2luY2x1ZGUJPHN0ZGlvLmg+DQogaW50CQltYWluKGludCBhYywgY2hhciAqKmF2KQ0Kew0KICBpbnQJCWk7DQogIEZJTEUJCSpmcHRyOw0KICBjaGFyCQlmbls1MF07DQogIGNoYXIJCXN0cltdID0gInJ1bm5lciBSb2Nrc1xuIjsNCiAgDQogIGZwdHIgPSBmb3Blbigib3V0Lmpzb24iLCAidysiKTsNCiAgDQogIGZvciAoaSA9IDA7IHN0cltpXSAhPSAnXG4nOyBpKyspDQogICAgZnB1dGMoc3RyW2ldLCBmcHRyKTsNCiAgDQogIGZjbG9zZShmcHRyKTsNCiAgcmV0dXJuIDA7DQp9DQo=',
                 'language': 'c'}

    prod.producer.send(INPUT_TOPIC, test_real).get()


