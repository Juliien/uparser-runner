import json
import os

print(os.getcwd())

SOURCE_PATHNAME = "ressources/mock_parsing_data/MOCK_DATA.json"
DESTINATION_PATHNAME = "src/ressources/"
with open(SOURCE_PATHNAME) as json_file:
    data = json.load(json_file)
    for d in data:
        print(d)
