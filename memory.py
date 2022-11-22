import json

TRAINING_FILE = "words.json"
RESPONSE_FILE = "responses.json"
MEMORY_FILE = None

class Memory:
    def __init__(self):
        self.tag_dict = self.read_memory(TRAINING_FILE)
        self.responses = self.read_memory(RESPONSE_FILE)

    def read_memory(self, file):
        """Reads json file, returns the contents"""
        with open(file) as json_file:
            contents = json.load(json_file)
            json_file.close()
        return contents