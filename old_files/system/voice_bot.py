import pyaudio
import pyttsx3
import speech_recognition as sr
from bot import ChatBot

class VoiceBot(ChatBot):
    def __init__(self, front_lobe="chat"):
        ChatBot.__init__(self, front_lobe)
        self.__listener = sr.Recognizer()
        self.__vocals = pyttsx3.init()
        self.__voice_recognition = False
        self.__voice = False
    
    def say_text(self, message):
        """If bot has voice recognition active, speaks the message"""
        if self.__voice:
            self.__vocals.say(message)
            self.__vocals.runAndWait()

    def audio_to_text(self):
        """Returns a dictionary of possible phrases the program recognized through the device's microphone"""
        with sr.Microphone() as source:
            self.say_text("Say your option")
            audio = self.__listener.listen(source)
            detected_phrases = self.__listener.recognize_google(audio, show_all=True)
            if not detected_phrases:
                self.say_text("Couldn't catch that, wait one second after the speaking cue and try again")
                return None
            else:
                phrases = [phrase["transcript"] for phrase in detected_phrases["alternative"]]
                return phrases    

    def get_voice_recognition(self):
        """Returns the state of voice recognition (if it is on or off)"""
        return self.__voice_recognition

    def set_voice_recognition(self, setting):
        """Turns voice recognition on or off; if on, adjusts the energy level to the background noise"""
        self.__voice_recognition = setting
        self.__listener.dynamic_energy_threshold = setting        
        if setting:
            with sr.Microphone() as source:
                self.__listener.adjust_for_ambient_noise(source, duration=2)

    def get_voice(self):
        """Returns bot's voice state"""
        return self.__voice

    def set_voice(self, setting):
        """Turns bot's voice on or off"""
        self.__voice = setting