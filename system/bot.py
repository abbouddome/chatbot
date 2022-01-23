from brain.cerebral import CerebralCortex

class ChatBot():
    def __init__(self, frontal_junct="chat"):
        self.__brain = CerebralCortex(frontal_junct)
        self.__user = {}
        self.__secondary_command = None

    def set_user(self, user_data):
        if user_data is not None:
            self.__user = user_data

    def get_user(self):
        return self.__user

    def set_secondary(self, command):
        self.__secondary_command = command

    def get_secondary(self):
        return self.__secondary_command

    def text_recognition(self, phrases, training=False):
        """Takes a list of phrases, returns a guess as to what it means"""
        thoughts = self.__brain.process_text(phrases, self.__secondary_command, training)
        user_data = thoughts["user"]
        if user_data:
            if self.__user.get("name") != user_data.get("name"):
                self.set_user(thoughts.get("user"))
        if self.__user:
            self.__brain.remember_user(self.__user)
        del thoughts["user"]
        return thoughts

    def change_mode(self, frontal_junct):
        """Changes the frontal_junct variable in the frontal lobe"""
        self.__brain.frontal_lobe.adaptive_memory(frontal_junct)

a = ChatBot()
print(a.text_recognition("Hi"))