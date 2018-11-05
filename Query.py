import sys
import listUtils
import ast
from termGenerator import TermGenerator


def process_query(query, index, termGenerator):

    # apply to query the same procedure for generating terms that we did when creating the index
    terms = termGenerator.generate_terms(query)

    # output file that will contain the final query result
    outputFile = open('./output/queryResult.txt', 'w')

    if len(terms) == 0:
        # this will happen when the user query contains only stop words (because stop words are discarded)
        print('No documents satisfy your query')

    if len(terms) == 1:
        print('Documents that satisfy your query:')
        for doc in index[terms[0]]:
            print(doc)
            outputFile.write(doc + '\n')

    elif len(terms) > 1:

        # sort query terms by posting list length to optimize computation
        terms.sort(key=lambda t: len(index[t]))

        docs = listUtils.intersect_lists(index[terms[0]], index[terms[1]])
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


def read_index_from_file(filename):
    index = {}
    print('Reading index from file', filename)
    with open(filename) as indexRaw:
        # line has the following format
        # term:[doc1, doc2, doc3]
        for line in indexRaw:
            lineParts = line.rsplit(':', 1)
            term = lineParts[0]
            postingsList = ast.literal_eval(lineParts[1])
            index[term] = postingsList

    return index


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('\nHow to use this program:')
        print('Query index_path term1 term2 term3 ...\n')
        print('Example: "Query ./output/outputIndex.txt stanford computer science" will retrieve all '
              'documents which contain these three words, using the index stored at the index_path. \n'
              'Query result can also be found in ./output/queryResult.txt\n')
        exit(1)

    indexPath = sys.argv[1]
    query = ' '.join(sys.argv[2:])
    # query = 'stanford computer science'

    # read index from file
    index = read_index_from_file(indexPath)

    # process the query
    process_query(query, index, TermGenerator())
