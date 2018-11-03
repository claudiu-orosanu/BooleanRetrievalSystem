from simpleIndexer import SimpleIndexer

if __name__ == '__main__':

    pathToBaseFolder = './real_data/0/'

    indexer = SimpleIndexer(pathToBaseFolder, True)
    indexer.index()

    print(indexer.dictionary)
    indexer.writeIndexToFile('outputIndex.txt')



