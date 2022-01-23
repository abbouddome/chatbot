from collections import Counter
import itertools
import math
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize


class FrontalLobe:
    def __init__(self):
        self.wernicke_area = WordNetLemmatizer()
        self.frontal_junct = None
        self.labels = None
        self.all_keywords = None
        self.keywords = None
        self.download_libraries()

    def download_libraries(self):
        """Downloads libraries used with NLTK"""
        nltk.download('averaged_perceptron_tagger')
        nltk.download("wordnet")
    
    def to_bool(self, command):
        """Turns the command yes or no to its boolean form"""
        if command == "yes":
            return True
        elif command == "no":
            return False
        else:
            return command

    def classify_importance(self):
        """Generates the weight for each word in each classifier in the classifier dictionary"""
        doc_freq, word_freq = self.count_words(relevant_labels)
        log_base = len(doc_freq)
        weights = {}
        something = {}

        for label, freq_table in something.items():
            label_entry = {}
            for word, freq in freq_table.items():
                tf = math.log(1 + freq, 1 + sum(freq_table.values()))
                df = math.log(1 + freq, 1 + word_freq[word])
                idf = math.log(log_base / doc_freq[word], log_base)
                label_entry[word] = tf * df * idf ** 2
            weights[label] = label_entry
    
        return weights

    def process_text(self, phrase):
        """Takes a phrase (string) and returns a dictionary with filtered root words, the original sentence and the word tags"""
        tokenized = [word.title() for word in word_tokenize(phrase)]
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

    def naive_bayes(self, phrase):
        """Uses the Naive Bayes algorithm to return a command; also returns its list of lemmas"""
        probabilities = {}
        normalizer = 0
        weights = self.classify_importance()

        for label, vocab in weights.items():
            bag_of_words = [phrase.count(word) for word in vocab.keys()]
            semi_mult = [-1 * prob * word * 1 / (math.log(prob)) for word, prob in zip(bag_of_words, vocab.values()) if word != 0]
            if semi_mult != []:
                probabilities[label] = sum(semi_mult)
                normalizer += probabilities[label]
        probabilities = {label: prob / normalizer for label, prob in probabilities.items()}
        
        if probabilities:
            command = max(probabilities, key=probabilities.get)
            if probabilities[command] >= 0.35:
                return self.to_bool(command)
        else:
            return None

    def find_name(self, word_tags):
        """Finds a name in a list of lemmas"""
        for word, tag in word_tags:
            if tag == "NNP":
                return word
        return None