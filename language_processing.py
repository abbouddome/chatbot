from collections import Counter
import itertools
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer


class LanguageProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.frontal_junct = None
        self.labels = None
        self.all_keywords = None
        self.keywords = None
        self.stopwords = stopwords.words("english")
        self.download_libraries()

    def download_libraries(self):
        """Downloads libraries used with NLTK"""
        nltk.download('punkt')
        nltk.download("stopwords")
        nltk.download('averaged_perceptron_tagger')
        nltk.download("wordnet")

    def process_text(self, phrase):
        """Takes a phrase (string) and returns a dictionary with filtered root words, the original sentence and the word tags"""
        tokenized = [word for word in word_tokenize(phrase)]
        word_tags = nltk.pos_tag(tokenized)
        lemmas = []
        for word, tag in word_tags:
            if tag in ["NN", "NNS", "NNP", "NNPS", "PRP", "$"]:
                word = self.__wernicke_area.lemmatize(word.lower(), "n")
            elif tag in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]:
                word = self.__wernicke_area.lemmatize(word.lower(), "v")
            elif tag in ["JJ", "JJR", "JJS", "WRB", "RB", "RBR", "RBS", "CD", "WP", "UH", "DT"]:
                word = self.__wernicke_area.lemmatize(word.lower(), "a")
            else:
                continue
            lemmas.append(word)
        return {"lemmas": lemmas, "tags": word_tags, "phrase": tokenized}