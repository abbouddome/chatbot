from .database.files import FileHandler

class Hippocampus():
    def __init__(self):
        self.__gyrus = FileHandler()
        self.retrieve_memories()

    def retrieve_memories(self):
        """Initializes the brain's memory variables"""
        self.__labels = self.__gyrus.read_json("training_data.json")
        self.__all_keys = self.__gyrus.read_json("keywords.json")
        self.__explicit_memory = self.__gyrus.read_json("memory.json")
        self.__all_responses = self.__gyrus.read_json("responses.json")

    def store_labels(self, labels):
        """Stores labels in the database"""
        self.__labels = labels
        self.__gyrus.write_json("training_data.json", self.__labels)

    def store_all_keys(self, all_keys):
        """Stores all keys in the database"""
        self.__all_keys = all_keys
        self.__gyrus.write_json("keywords.json", self.__all_keys)

    def store_explicit_memory(self, explicit_memory):
        """Stores explicit memory in the database"""
        self.__explicit_memory = explicit_memory
        self.__gyrus.write_json("memory.json", self.__explicit_memory)

    def send_memories(self):
        """Returns the packed memories"""
        packed_memories = [self.__labels, self.__all_keys, self.__explicit_memory, self.__all_responses] 
        return packed_memories