# import json
# import os
import base64

VALID_EXTENSION = ["csv", "json"]


# check syntax and extension of source and destination file
def create_dest_name_from_source(self, source_filename: str, extension: str):
    self.source_name = source_filename
    split = source_filename.split('.')
    file_name = split[0]
    extention = split[1]
    if extention not in VALID_EXTENSION:
        raise Exception
    self.dest_name = file_name + extension

def decode(todecode):
    return base64.b64decode(todecode)


def encode(toencode):
    return base64.b64encode(toencode)


def consume():
    return {'id': '1234', 'from': 'json', 'to': 'csv',
            'inputfile': 'eyAnaGVsbG8nOiAnd29ybGQnfQ==', 'algorithm': 'cHJpbnQoImhlbGxvIHdvcmxkISIp', 'language': 'python'}

# print(os.getcwd())
#
# SOURCE_PATHNAME = "ressources/mock_parsing_data/MOCK_DATA.json"
# DESTINATION_PATHNAME = "src/ressources/"
# with open(SOURCE_PATHNAME) as json_file:
#     data = json.load(json_file)
#     for d in data:
#         print(d)
