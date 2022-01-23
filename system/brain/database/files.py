import os
import json


class FileHandler():
    def __init__(self):
        self._path = os.path.dirname(__file__)

    def read_file(self, file_name):
        with open(file_name, "r") as file:
            return file.readlines()

    def read_json(self, file_name):
        file_path = "{}\\{}".format(self._path, file_name)
        with open(file_path, "r") as file:
            return json.load(file)

    def write_json(self, file_name, data):
        file_path = "{}\\{}".format(self._path, file_name)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4) 