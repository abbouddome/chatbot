from language_processing import LanguageProcessor
from memory import Memory
from profile import Profile
from collections import defaultdict, Counter
import math
import itertools
import random

class Processor:
    def __init__(self):
        self.memory = Memory()
        self.language_processor = LanguageProcessor()
        self.tag_frequencies = self.language_processor.parse_memory(self.memory.tag_dict)
        self.profile = Profile()

    def generate_word_counts(self):
        """Generates a dictionary with words as a key and the number of times they appear in all tags as values"""
        all_words = Counter()
        for freq_table in self.tag_frequencies.values():
            all_words += Counter(freq_table)
        doc_freq = dict(Counter(itertools.chain.from_iterable(map(set, self.tag_frequencies.values()))))
        return doc_freq, dict(all_words)

    def generate_weighted_features(self):
        """Generates a dictionary of weighted features (feature * weight)"""
        doc_freq, all_words = self.generate_word_counts()
        log_base = len(self.tag_frequencies.keys())
        features = {}
        for tag, freq_table in self.tag_frequencies.items():
            tag_entry = {}
            for word, freq in freq_table.items():
                tf = math.log(1 + freq, 1 + sum(freq_table.values()))       #frequency in tag / total words in tag
                df = math.log(1 + freq, 1 + all_words[word])                #frequency in tag / total number of that word
                idf = math.log(log_base / doc_freq[word], log_base)         #log(total tags / total times word in all tags)
                tag_entry[word] = tf * df * idf ** 2
            features[tag] = tag_entry
        return features

    def generate_entropy(self, phrase, weighted_features):
        """Generates the entropy of the weighted features"""
        entropy = defaultdict(int, { key: 0 for key in weighted_features.keys()})
        for tag, vocabulary in weighted_features.items():
            bag_of_words = [phrase.count(word) for word in vocabulary.keys()]
            for is_present, weighted_feature in zip(bag_of_words, vocabulary.values()):
                if is_present != 0:
                    entropy[tag] += -1 * is_present * weighted_feature * 1 / math.log(weighted_feature)
        denominator = sum(entropy.values())
        if denominator != 0:
            for tag in entropy.keys():
                entropy[tag] /= denominator
        return entropy

    def max_entropy(self, phrase):
        """Finds the tag with the highest entropy"""
        weighted_features = self.generate_weighted_features()
        entropy = self.generate_entropy(phrase, weighted_features)
        if max(entropy.values()) >= 0.35:
            return max(entropy, key=entropy.get)
        return "None"

    def text_recognition(self, phrase):
        """"""
        lemmas = self.language_processor.process_text(phrase)
        tag = self.max_entropy(lemmas)
        return tag

    def generate_response(self, phrase, tag):
        if tag == "Name":
            self.profile.name = self.language_processor.find_name(phrase)
        elif tag == "MName":
            if self.profile.name:
                return (self.memory.responses["MNameY"] + self.profile.name)
            else:
                tag = "MNameN"
        elif tag == "Weight" or tag == "Height" or tag == "Age":
            number = self.language_processor.find_number(phrase)
            if tag == "Weight":
                self.profile.weight = number
            if tag == "Height":
                self.profile.height = number
            else:                
                self.profile.age = number
        return random.choice(self.memory.responses[tag])


