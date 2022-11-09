from processor import Processor

class ChatBot():
    def __init__(self):
        self.processor = Processor()

    def response(self, phrases):
        """Takes a phrase, returns a guess as to what it means"""
        thoughts = self.processor.process_text()


        """
        Get text
        Understand text

        """