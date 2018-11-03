import os
import collections
import string

# natural language toolkit
import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords

stemmer = PorterStemmer()
# nltk.download('stopwords')

class SimpleIndexer:

    def __init__(self, pathToBaseFolder, debug = False):
        self.dictionary = {}
        self.pathToBaseFolder = pathToBaseFolder
        self.debug = debug

    def index(self):

        # traverse all files in base directory and its subdirectories
        for root, dirs, files in os.walk(self.pathToBaseFolder):
            for filename in files:
                with open(os.path.join(root, filename)) as file:
                    self.log('--------------------Processing words in file:', os.path.join(root, filename), '--------------------')

                    # read file text
                    text = file.read()
                    self.log('Original text')
                    self.log(text)

                    # generate tokens
                    tokens = self.generate_tokens(text)

                    # add tokens to dictionary
                    self.log('Adding tokens to dictionary...')
                    self.add_tokens_to_dictionary(os.path.join(root, filename), tokens)

                    self.log(self.dictionary)

                    self.log('\n\n\n')

                break

        # sort dictionary values to facilitate merging of posting lists
        for token in self.dictionary:
            self.dictionary[token] = sorted(self.dictionary[token])

    def generate_tokens(self, text):
        # tokenize: split string by punctuation marks also (not only spaces)
        self.log('Tokenizing...')
        tokens = nltk.word_tokenize(text)
        self.log(tokens)

        self.log('Processing tokens...')
        tokens = self.process_tokens(tokens)
        self.log('Processing tokens... Done')

        return tokens

    def process_tokens(self, tokens):
        # normalize tokens
        tokens = self.normalize_tokens(tokens)
        self.log('Normalizing...')
        self.log(tokens)

        # stem tokens
        tokens = self.stem_tokens(tokens)
        self.log('Stemming...')
        self.log(tokens)

        # remove stop words
        self.log('Removing stop words...')
        tokens = self.remove_stop_words(tokens)
        self.log(tokens)

        # remove duplicates and sort tokens
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

        return tokens

    def stem_tokens(self, tokens):
        tokens = [stemmer.stem(token) for token in tokens]
        return tokens

    def remove_stop_words(self, tokens):
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        return tokens

    def writeIndexToFile(self, filePath):
        with open(filePath, 'w') as file:
            for word, postingList in self.dictionary.items():
                file.write(word + ':' + str(postingList) + '\n')

    def log(self, *args):
        if self.debug:
            print(' '.join([str(e) for e in args]))

    def add_tokens_to_dictionary(self, docId, tokens):
        for token in tokens:

            # if token is not in dictionary, add it
            if token not in self.dictionary:
                self.dictionary[token] = []

            self.dictionary[token].append(docId)



