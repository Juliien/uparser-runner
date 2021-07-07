import base64


def decode(todecode):
    return base64.b64decode(todecode)


def encode(toencode):
    return base64.b64encode(toencode)
