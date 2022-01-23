from brain import Brain

class ChatBot():
    def __init__(self):
        self.brain = Brain()


    def text_recognition(self, phrases, training=False):
        """Takes a phrase, returns a guess as to what it means"""
        thoughts = self.brain.process_text()


        """
        Get text
        Understand text

        """