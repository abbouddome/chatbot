from .hippocampus import Hippocampus
from .frontal_lobe import FrontalLobe
from .temporal_lobe import TemporalLobe

class CerebralCortex():
    def __init__(self, frontal_junct):
        self.hippocampus = Hippocampus()
        self.frontal_lobe = FrontalLobe()
        self.temporal_lobe = TemporalLobe()
        self.__cache = [None] * 4
        self.init_memories()
        self.frontal_lobe.adaptive_memory(frontal_junct)

    def init_memories(self):
        """Collects memories from hippocampus and distributes to other parts of brain"""
        memories = self.hippocampus.send_memories()
        self.frontal_lobe.recieve_memories(memories[0:2])
        self.temporal_lobe.recieve_memories(memories[2:4])

    def remember_user(self, user_data):
        """Stores the updated user data in explicit memory"""
        explicit_memory = self.temporal_lobe.get_explicit_memory()
        key = user_data["name"]
        explicit_memory[key] = user_data
        self.hippocampus.store_explicit_memory(explicit_memory)
        self.init_memories()

    def add_to_cache(self, word):
        """Adds command to cache; after four entries, deletes the first entry"""
        if len(self.__cache) == 4:
            del self.__cache[0]
        if word:
            self.__cache.append(word)

    def supervised_train(self, command, phrase):
        """Train the bot via supervised learning in the command line"""
        label_entry = {}
        labels = self.frontal_lobe.get_labels()
        all_keywords = self.frontal_lobe.get_all_keys()
        print("{}: {}".format(command, phrase))
        if input("Is this command correct? ") == "n":
            command = input("Type correct command: ")
        if command in labels.keys():
            label_entry = labels[command]
        for word in phrase:
            if word in label_entry.keys():
                label_entry[word] += 1
            else:
                if input("Insert '" + word + "' in dictionary? ") == "y":
                    label_entry[word] = 1
        key_check = input("What key is this in? ")
        if key_check != "":
            if key_check not in all_keywords.keys():
                all_keywords[key_check] = [command]
            else:
                if command not in all_keywords[key_check]:
                    all_keywords[key_check].append(command)
        labels[command] = label_entry
        self.hippocampus.store_labels(labels)
        self.hippocampus.store_all_keys(all_keywords)        
        self.init_memories()

    def process_text(self, phrases, secondary, training):
        """Takes phrases, returns a dictionary of thoughts as to what the brain deduced it means"""
        if type(phrases) is str:
            phrases = [phrases]
        for phrase in phrases:
            phrase_data = self.frontal_lobe.process_text(phrase)
            lemmas = phrase_data.get("lemmas")
            command = self.frontal_lobe.naive_bayes(lemmas)
            if training is True:
                self.supervised_train(command, lemmas)
            else:
                if command == "name" or secondary == "name":
                    phrase_data["name"] = self.frontal_lobe.find_name(phrase_data.get("tags"))
                    if phrase_data["name"] is not None:
                        command = "name"
                elif secondary == "choice":
                    command = secondary    
            if command is not None or phrase == phrases[-1]:
                expressions = self.temporal_lobe.articulate_speech(command, phrase_data, self.__cache)
                self.add_to_cache(command)
                self.frontal_lobe.adaptive_memory(expressions.get("frontal_junct"))
                return {"cmd": command, "words": lemmas, "msg": expressions.get("msg"), "user": expressions.get("user")}