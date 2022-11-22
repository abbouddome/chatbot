from collections import Counter, defaultdict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import re

class LanguageProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = stopwords.words("english")
        self.download_libraries()

    def download_libraries(self):
        """Downloads libraries used with NLTK"""
        nltk.download('punkt')
        nltk.download("stopwords")
        nltk.download('averaged_perceptron_tagger')
        nltk.download("wordnet")
        nltk.download("omw-1.4")
        nltk.download('maxent_ne_chunker')
        nltk.download('words')

    def parse_memory(self, memory):
        """Generates the frequencies of words for each tag"""
        tags = defaultdict(dict)
        for tag, phrases in memory.items():
            total_count = Counter()
            for phrase in phrases:
                total_count += Counter(self.process_text(phrase))
            tags[tag] = dict(total_count)
        return tags

    def process_text(self, phrase):
        """Takes a phrase (string) and returns a dictionary with filtered root words, the original sentence and the word tags"""
        tokenized = word_tokenize(phrase)
        word_tags = nltk.pos_tag(tokenized)
        lemmas = []
        for word, tag in word_tags:
            if tag in ["NN", "NNS", "NNP", "NNPS", "PRP", "$"]:
                word = self.lemmatizer.lemmatize(word.lower(), "n")
            elif tag in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]:
                word = self.lemmatizer.lemmatize(word.lower(), "v")
            elif tag in ["JJ", "JJR", "JJS", "WRB", "RB", "RBR", "RBS", "CD", "WP", "UH", "DT"]:
                word = self.lemmatizer.lemmatize(word.lower(), "a")
            else:
                continue
            lemmas.append(word)
        #return {"lemmas": lemmas, "tags": word_tags, "phrase": tokenized}
        return lemmas

    def find_name(self, phrase):
        """Finds name in phrase and returns it"""
        tokenized = word_tokenize(phrase)
        word_tags = nltk.pos_tag(tokenized)
        name = ""
        for result in nltk.ne_chunk(word_tags):
            if type(result) == nltk.Tree:
                for leaf in result.leaves():
                    name += leaf[0] + " "
        return name

    def find_number(self, phrase):
        numbers = [int(i) for i in re.findall(r'\b\d+\b', phrase)]
        return numbers[0]