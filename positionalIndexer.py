import os


def tokenizeWord(word: str) -> str:
    # make word lowercase
    word = word.lower()

    return word


class PositionalIndexer:

    def __init__(self, pathToBaseFolder):
        self.dictionary = {}
        self.pathToBaseFolder = pathToBaseFolder

    def index(self):

        for filename in os.listdir(self.pathToBaseFolder):
            with open(self.pathToBaseFolder + filename) as file:

                words = [word for line in file for word in line.split()]
                for i in range(0, len(words)):
                    word = words[i]
                    pos = i

                    # tokenize word
                    word = tokenizeWord(word)

                    # if word is not in dictionary, add it
                    if word not in self.dictionary:
                        self.dictionary[word] = {}

                    # if word posting list does not contain this document, add it
                    if filename not in self.dictionary[word]:
                        self.dictionary[word][filename] = []

                    # add position for this word in this document
                    self.dictionary[word][filename].append(pos)

        for word, postingList in self.dictionary.items():
            print(word, postingList)

    def writeIndexToFile(self, filePath):
        with open(filePath, 'w') as file:
            for word, postingList in self.dictionary.items():
                file.write(word + ':' + str(postingList) + '\n')
