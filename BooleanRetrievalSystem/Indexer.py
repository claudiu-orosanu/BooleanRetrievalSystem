import sys

from simpleIndexer import SimpleIndexer
from termGenerator import TermGenerator
import datetime

# Uncomment this to download nltk data
# nltk.download('punkt')
# nltk.download('stopwords')


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('\nHow to use: Indexer corpus_dir_path out_index_path\n')
        print('Example: Indexer ./real_data ./output/outputIndex.txt\n')
        exit(1)

    pathToBaseFolder = sys.argv[1]
    outputPath = sys.argv[2]

    # show logs or not
    debugMode = False

    print('Creating index...')
    # this object will generate the terms from raw text
    termGenerator = TermGenerator(debugMode)

    # this object will create the index
    chunkSize = 500000
    indexer = SimpleIndexer(pathToBaseFolder, termGenerator, chunkSize, debugMode)

    startTime = datetime.datetime.now()
    print('Start time', startTime)

    # create index
    indexer.create_index()

    endTime = datetime.datetime.now()
    print('End time', endTime)

    print('It took', (endTime - startTime).total_seconds())
