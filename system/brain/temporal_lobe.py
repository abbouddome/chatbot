import requests
import random

class TemporalLobe():
    def __init__(self):
        self.__working_memory = {}
        self.__explicit_memory = None
        self.__all_responses = None
        self.__connected = self.check_connection()

    def recieve_memories(self, memory):
        """Sets the local memory to memory values passed"""
        self.__explicit_memory = memory[0]
        self.__all_responses = memory[1]

    def check_connection(self):
        """Sets connected depending on if the computer is connected to an internet connection"""
        try:
            requests.get("http://jsonip.com", timeout=3)
            self.__connected = True            
        except (requests.ConnectionError, requests.Timeout):
            self.__connected = False

    def quick_response(self, command):
        """Gets a command, generates a quick response"""
        if command in self.__all_responses.keys():
            message = random.choice(self.__all_responses[command])
        else:
            message = random.choice(self.__all_responses["none"])
        return {"msg": message}

    def make_greeting(self):
        message = random.choice(self.__all_responses["greet"])
        return {"msg": (message + " How can I help?")}

    def binary_command(self, command, previous):
        """Special commands for yes and no commands"""
        thoughts = {}
        if previous == "name":
            if command is True:
                message = random.choice(self.__all_responses["recognize"]["greet"])
                user =  self.__working_memory["user"]
            else:
                message = random.choice(self.__all_responses["name"])
                user =  self.__working_memory["new_user"]
            thoughts = {"msg": message, "frontal_junct": "chat", "user": user}
        return thoughts
    
    def recognize_name(self, name):
        """If user's name is in the explicit memory, places user's data in recognition memory"""
        if name is not None:
            new_user = {"name": name, "wins": 0, "losses": 0}
            self.__working_memory["new_user"] = new_user
            recognize_set = self.__all_responses["recognize"]
            if name in self.__explicit_memory.keys():
                user = self.__explicit_memory[name]
                if user["wins"] > user["losses"]:
                    message = random.choice(recognize_set["won"])
                elif user["wins"] < user["losses"]:
                    message = random.choice(recognize_set["lose"])
                else:
                    message = random.choice(recognize_set["neutral"])
                thoughts = {"msg": message, "frontal_junct": "bin"}
                self.__working_memory["user"] = user
            else:
                new_user = {"name": name, "wins": 0, "losses": 0}
                message = random.choice(self.__all_responses["name"])
                thoughts = {"msg": message, "user": new_user}
        else:
            message = random.choice(self.__all_responses["none"])
            thoughts = {"msg": message}
        return thoughts

    def articulate_speech(self, command, phrase_data, cache):
        """Gets a command, list of lemmas and cache, and returns the bot's responses"""
        if command is True or command is False:
            return self.binary_command(command, cache[-1])
        elif command == "name":
            return self.recognize_name(phrase_data.get("name"))
        elif command == "choice":
            return {"msg": phrase_data.get("phrase")}
        elif command == "greet":
            return self.make_greeting()
        else:
            return self.quick_response(command)

    def get_explicit_memory(self):
        return self.__explicit_memory