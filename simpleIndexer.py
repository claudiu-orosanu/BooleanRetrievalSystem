import os
import collections
import string


class SimpleIndexer:

    def __init__(self, pathToBaseFolder, termGenerator, debugMode=False):
        self.index = {}
        self.pathToBaseFolder = pathToBaseFolder
        self.debugMode = debugMode
        self.termGenerator = termGenerator

    def create_index(self):

        count = 0
        # traverse all files in base directory and its subdirectories
        for root, dirs, files in os.walk(self.pathToBaseFolder):
            for filename in files:
                with open(os.path.join(root, filename)) as file:
                    self.log('--------------------Processing words in file:', os.path.join(root, filename), '--------------------')

                    # read file text
                    text = file.read()
                    self.log('Original text')
                    self.log(text)

                    # generate terms
                    terms = self.termGenerator.generate_terms(text)

                    # add terms to index
                    self.log('Adding terms to dictionary...')
                    self.add_terms_to_index(os.path.join(root, filename), terms)

                    self.log(self.index)

                    self.log('\n\n\n')

                # count += 1
                # if count > 20:
                #     break

        # sort index values to facilitate merging of posting lists
        for term in self.index:
            self.index[term] = sorted(self.index[term])

    def write_index_to_file(self, filePath):
        with open(filePath, 'w') as file:
            for word, postingList in self.index.items():
                file.write(word + ':' + str(postingList) + '\n')

    def log(self, *args):
        if self.debugMode:
            print(' '.join([str(e) for e in args]))

    def add_terms_to_index(self, docId, terms):
        for term in terms:

            # if terms is not in index, add it
            if term not in self.index:
                self.index[term] = []

            self.index[term].append(docId)



