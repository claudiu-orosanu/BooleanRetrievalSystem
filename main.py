from simpleIndexer import SimpleIndexer
from termGenerator import TermGenerator
import listUtils
import datetime

# Uncomment this to download nltk data
# nltk.download('punkt')
# nltk.download('stopwords')


def process_query(query, index, termGenerator):
    terms = termGenerator.generate_terms(query)
    outputFile = open('queryResult.txt', 'w')

    if len(terms) == 1:
        print('Documents that satisfy your query:')
        for doc in index[terms[0]]:
            print(doc)
            outputFile.write(doc + '\n')

    elif len(terms) > 1:
        docs = listUtils.intersect_lists(index[terms[0]], index[terms[1]])
        # TODO optimize this query (intersect the smallest posting lists every time)
        for i in range(2, len(terms)):
            docs = listUtils.intersect_lists(docs, index[terms[i]])

        if len(docs) == 0:
            print('No document satisfies your query')
        else:
            print('Documents that satisfy your query:')
            for doc in docs:
                print(doc)
                outputFile.write(doc + '\n')

    outputFile.close()


if __name__ == '__main__':
    pathToBaseFolder = './real_data/0/'

    print('Creating index...')
    termGenerator = TermGenerator(False)
    indexer = SimpleIndexer(pathToBaseFolder, termGenerator, False)

    startTime = datetime.datetime.now()
    print('Start time', startTime)

    # start indexing process
    indexer.create_index()

    # write index to file
    indexer.write_index_to_file('outputIndex.txt')

    # init query TODO provide this as cmd argument
    query = 'stanford computer science'

    # process the query
    process_query(query, indexer.index, termGenerator)

    endTime = datetime.datetime.now()
    print('End time', endTime)

    print('It took', (endTime - startTime).total_seconds())
