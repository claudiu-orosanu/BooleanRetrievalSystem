import ast
import os
import collections
import sys


class SimpleIndexer:

    def __init__(self, pathToBaseFolder, termGenerator, chunkSize, debugMode=False):
        self.index = {}
        self.pathToBaseFolder = pathToBaseFolder
        self.termGenerator = termGenerator
        self.chunkSize = chunkSize
        self.debugMode = debugMode

    def create_index(self):

        count = 0
        chunkNumber = 0
        # traverse all files in base directory and its subdirectories
        for root, dirs, files in os.walk(self.pathToBaseFolder):
            for filename in files:
                with open(os.path.join(root, filename)) as file:
                    self.log('--------------------Processing words in file:', os.path.join(root, filename), '--------------------')

                    count += 1
                    if count % 500 == 0:
                        print('Currently at file...', count)

                    # read file text
                    text = file.read()
                    self.log('Original text')
                    self.log(text)

                    # generate terms
                    terms = self.termGenerator.generate_terms(text)

                    # add terms to index
                    self.log('Adding terms to dictionary...')
                    self.add_terms_to_index(os.path.join(root, filename), terms)

                    if sys.getsizeof(self.index) > self.chunkSize:
                        self.sort_index()
                        self.write_index_chunk(chunkNumber)
                        self.index = {}
                        chunkNumber += 1

                    self.log('\n\n\n')

                # if count > 50:
                #     break

        # write remaining terms to disk
        if len(self.index) > 0:
            self.sort_index()
            self.write_index_chunk(chunkNumber)
            chunkNumber += 1

        # merge chunks into final index
        print('--------------------Index chunks written to disk:', '--------------------')
        print('--------------------Merging index chunks into ./output/outputIndex.txt--------------------')
        self.merge_chunks(chunkNumber)

    def add_terms_to_index(self, docId, terms):
        for term in terms:

            # if term is not in index, add it
            if term not in self.index:
                self.index[term] = []

            self.index[term].append(docId)

    def sort_index(self):
        # sort index values alphabetically
        self.index = collections.OrderedDict(sorted(self.index.items()))
        # sort values for every key to facilitate merging of posting lists
        for term in self.index:
            self.index[term] = sorted(self.index[term])

    def write_index_chunk(self, chunkNumber):
        path = './index_chunks/'
        path += f"index-chunk-{chunkNumber}.txt"
        print('Writing index chunk to disk:', path)
        with open(path, 'w') as file:
            for term in self.index:
                file.write(f"{term}:{self.index[term]}\n")

    def log(self, *args):
        if self.debugMode:
            print(' '.join([str(e) for e in args]))

    def merge_chunks(self, chunkNumber):

        # open files that contain index chunks
        chunks = []
        count = 0
        for chunkFileName in os.listdir('./index_chunks/'):
            chunks.append(open('./index_chunks/' + chunkFileName))
            count += 1
            if count == chunkNumber:
                break

        finalIndexPath = './output/outputIndex.txt'
        chunksIndex = {}
        finalIndexFile = open(finalIndexPath, 'w')

        """
            In the following code we will iterate through each chunk one term at a time.
            
            For example, if we have 6 chunks, we will start with 6 terms and we will write the 
            smallest (lexicographically) term into the final index file.
            
            If the smallest term is currently in 2 of the 6 chunks, we have to merge the posting lists.
            
            After writing a pair of term:posting_list corresponding to each (or multiple) chunks we
            need to advance the respective chunks to the next term (line).
        """

        # iterate each chunk one term at a time
        for i in range(0, len(chunks)):
            line = chunks[i].readline()
            term, pList = line.rsplit(':', 1)
            pList = ast.literal_eval(pList)
            chunksIndex[i] = [term, pList] # [0] is the term, [1] is the posting list for the i-th chunk

        while True:
            # get the smallest term from all chunks
            minTerm = min([value[0] for value in chunksIndex.values()])
            # if there are multiple chunks that have the same smallest term, the posting lists need to be merged
            smallestChunks = [chunkNumber for chunkNumber in chunksIndex if chunksIndex[chunkNumber][0] == minTerm]
            completePList = []
            for ch in smallestChunks:
                completePList.append(chunksIndex[ch][1])
            # flatten pList
            completePList = [item for sublist in completePList for item in sublist]
            # write line to final index
            lineToWrite = f"{minTerm}:{completePList}\n"
            finalIndexFile.write(lineToWrite)

            # advance consumed chunks by one element
            for ch in smallestChunks:

                # if chunk is finished, skip it
                if not chunks[ch]:
                    continue

                # read line from chunk
                line = chunks[ch].readline()
                if line:
                    term, pList = line.rsplit(':', 1)
                    pList = ast.literal_eval(pList)
                    chunksIndex[ch] = [term, pList]
                else:
                    # chunk finished
                    del chunksIndex[ch]
                    chunks[ch] = False # mark chunk as done

            # no more chunks -> done
            if len(chunksIndex.keys()) == 0:
                break

        finalIndexFile.close()


