from simpleIndexer import SimpleIndexer
import listUtils
import datetime


def process_query(query, indexer):
    tokens = indexer.generate_tokens(query)
    outputFile = open('queryResult.txt', 'w')
    if len(tokens) == 1:
        print('Documents that satisfy your query:')
        for doc in indexer.dictionary[tokens[0]]:
            print(doc)
            outputFile.write(doc + '\n')
    elif len(tokens) > 1:
        docs = listUtils.intersect_lists(indexer.dictionary[tokens[0]], indexer.dictionary[tokens[1]])
        for i in range(2, len(tokens)):
            docs = listUtils.intersect_lists(docs, indexer.dictionary[tokens[i]])

        if len(docs) == 0:
            print('No document satisfies your query')
        else:
            print('Documents that satisfy your query:')
            for doc in docs:
                print(doc)
                outputFile.write(doc + '\n')


if __name__ == '__main__':
    pathToBaseFolder = './real_data/0/'

    print('Creating index...')
    indexer = SimpleIndexer(pathToBaseFolder, False)

    print('Start time', datetime.datetime.now())
    indexer.index()

    indexer.writeIndexToFile('outputIndex.txt')

    query = 'stanford computer science'

    process_query(query, indexer)

    print('End time', datetime.datetime.now())
