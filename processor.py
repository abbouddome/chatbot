from language_processing import LanguageProcessor
from collections import defaultdict, Counter
import math

class Processor:
    def __init__(self):
        self.memory = None
        self.tag_dict = None
        self.language_processor = LanguageProcessor()

    def generate_all_words(self):
        """Generates a dictionary with words as a key and the number of times they appear in all tags as values"""
        all_words = Counter()
        for tag in self.tag_dict.items():
            all_words += Counter(tag)
        return all_words

    def generate_weighted_features(self):
        """Generates a dictionary of weighted features (feature * weight)"""
        all_words = self.generate_all_words()
        features = {}
        for tag, freq_table in self.tag_dict:
            tag_entry = {}
            for word, freq in freq_table.items():
                tf = freq / sum(freq_table.items()) #frequency in tag / total words in tag
                idf = math.log(len(self.tag_dict.keys()) / all_words[word]) #log(total tags / total times word in all tags)
                tag_entry[word] = tf * idf
            features[tag] = tag_entry
        return features

    def generate_entropy(self, phrase, weighted_features):
        """Generates the entropy of the weighted features"""
        entropy = defaultdict(int, { key: 0 for key in weighted_features.keys()})
        for tag, vocabulary in weighted_features.items():
            bag_of_words = [phrase.count(word) for word in vocabulary.keys()]
            for is_present, weighted_feature in zip(bag_of_words, vocabulary.values()):
                entropy[tag] += math.exp(is_present * weighted_feature)
        denominator = sum(entropy.values())
        for tag in entropy.keys():
            entropy[tag] /= denominator
        return entropy

    def max_entropy(self, phrase):
        """Finds the tag with the highest entropy"""
        weighted_features = self.generate_weighted_features()
        entropy = self.generate_entropy(phrase, weighted_features)
        return max(entropy, key=entropy.get)

    def generate_response(self, tag, phrase):
        pass

    def text_recognition(self, phrase):
        tag = self.max_entropy(phrase)
        response = self.generate_response(tag, phrase)
        return response

    def process_text(self):
        
        pass


