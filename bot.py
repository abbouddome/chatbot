from processor import Processor

class ChatBot():
    def __init__(self):
        self.processor = Processor()

    def response(self, phrase):
        """Takes a phrase, returns a guess as to what it means"""
        thoughts = self.processor.text_recognition(phrase)
        response = self.processor.generate_response(phrase, thoughts)
        return response

bot = ChatBot()
running = True
while running:
    user_input = input("Type: ")
    print(bot.response(user_input))