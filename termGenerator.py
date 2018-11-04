import string

# natural language toolkit
import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords


class TermGenerator:

    def __init__(self, debug=False):
        self.debug = debug
        self.stemmer = PorterStemmer()

    def generate_terms(self, text):
        """
        Generates terms from a string. These terms go through a process of tokenizing,
        normalizing and other language processing techniques

        :param text: The string from which terms are generated
        :return: The list of terms
        """
        # tokenize: split string by punctuation marks also (not only spaces)
        self.log('Tokenizing...')
        tokens = nltk.word_tokenize(text)
        self.log(tokens)

        self.log('Processing tokens...')
        terms = self.process_tokens(tokens)
        self.log('Processing tokens... Done')

        return terms

    def process_tokens(self, tokens):
        # normalize tokens
        tokens = self.normalize_tokens(tokens)
        self.log('Normalizing...')
        self.log(tokens)

        # stem tokens
        tokens = self.stem_tokens(tokens)
        self.log('Stemming...')
        self.log(tokens)

        # remove stop words -> after this queries containing stop words, like 'we are' (from example_queries), will fail
        self.log('Removing stop words...')
        tokens = self.remove_stop_words(tokens)
        self.log(tokens)

        # remove duplicates
        self.log('Removing duplicates...')
        tokens = list(dict.fromkeys(tokens))
        self.log(tokens)

        return tokens

    def normalize_tokens(self, tokens):
        # make all tokens lowercase
        tokens = [token.lower() for token in tokens]

        # discard punctuation marks
        tokens = [token for token in tokens if token not in string.punctuation]

        # discard numbers
        tokens = [token for token in tokens if not all(char.isdigit() for char in token)]

        # discard 's (appears in almost all documents)
        tokens = [token for token in tokens if token != "'s"]

        return tokens

    def stem_tokens(self, tokens):
        tokens = [self.stemmer.stem(token) for token in tokens]
        return tokens

    def remove_stop_words(self, tokens):
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        return tokens

    def log(self, *args):
        if self.debug:
            print(' '.join([str(e) for e in args]))




