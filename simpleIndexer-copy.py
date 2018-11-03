import os
import collections


def tokenizeWord(word: str) -> str:
    # make word lowercase
    word = word.lower()

    return word


class SimpleIndexer:

    def __init__(self, pathToBaseFolder):
        self.dictionary = {}
        self.pathToBaseFolder = pathToBaseFolder

    def index(self):

        # traverse all files in base directory and its subdirectories
        for root, dirs, files in os.walk(self.pathToBaseFolder):
            for filename in files:
                with open(os.path.join(root, filename)) as file:

                    # get all words in the file
                    words = [word for line in file for word in line.split()]

                    # create dictionary (inverted index)
                    for i in range(0, len(words)):
                        word = words[i]

                        # tokenize word
                        word = tokenizeWord(word)

                        # normalize word

                        # stemming

                        # discard stop words

                        # if word is not in dictionary, add it
                        if word not in self.dictionary:
                            self.dictionary[word] = []

                        # if word posting list does not contain this document, add it
                        if filename not in self.dictionary[word]:
                            self.dictionary[word].append(filename)

        # sort dictionary by keys
        self.dictionary = collections.OrderedDict(sorted(self.dictionary.items()))

        for word, postingList in self.dictionary.items():
            print(word, postingList)

    def writeIndexToFile(self, filePath):
        with open(filePath, 'w') as file:
            for word, postingList in self.dictionary.items():
                file.write(word + ':' + str(postingList) + '\n')
