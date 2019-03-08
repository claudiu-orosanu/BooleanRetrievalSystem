import datetime
import math
import re
import pickle
from collections import Counter, defaultdict

from sklearn.datasets import fetch_20newsgroups

read_saved_train_data = True


def tokenize(text):
    return re.findall(r'\b[a-zA-Z0-9]+\b', text)


def train(twenty_train):

    # prior probabilities of each class
    prior = Counter()

    # word frequency for each class
    cls_words_counter = defaultdict(Counter)

    # all unique words
    vocab = defaultdict()

    # iterate each document and store populate the data structures above
    for doc_idx, doc in enumerate(twenty_train.data):
        doc_class = twenty_train.target[doc_idx]
        prior[doc_class] += 1

        for word in tokenize(doc):
            cls_words_counter[doc_class][word] += 1
            vocab[word] = True

        # print(doc_idx)

    condprob = defaultdict(defaultdict)

    # this variables are for showing progress
    count = 0
    total = len(prior.keys()) * len(vocab)

    for cls in prior.keys():
        prior[cls] /= float(len(twenty_train.target))
        for word in vocab:
            
            condprob[cls][word] = \
                (1 + cls_words_counter[cls][word]) / (len(vocab) + sum(cls_words_counter[cls].values()))

            # measure progress
            count += 1
            if count % 25000 == 0:
                print('Training: ' + str(int(count/total * 100)) + '%')

    return prior, condprob, vocab


def predict(doc, prior, condprob, vocab):
    words = tokenize(doc)

    max_cls = (float('-inf'), 0)  # (prob, class_index)

    for cls in prior.keys():
        prob = math.log(prior[cls])

        for word in words:
            # consider only words that are present in vocabulary
            if word in vocab:
                prob += math.log(condprob[cls][word])

        if prob > max_cls[0]:
            max_cls = (prob, cls)

    # print(max_cls)
    return max_cls[1]


def main():
    twenty_train = fetch_20newsgroups(subset='train', shuffle=True,
                                      # categories=['alt.atheism', 'sci.space', 'talk.politics.guns', 'rec.autos']
                                      )

    start_time = datetime.datetime.now()
    print('Start time - training', start_time)

    if read_saved_train_data:
        # read train data from files (to avoid training every time)
        with open('prior.pkl', 'rb') as in_file:
            prior = pickle.load(in_file)
        with open('condprob.pkl', 'rb') as in_file:
            condprob = pickle.load(in_file)
        with open('vocab.pkl', 'rb') as in_file:
            vocab = pickle.load(in_file)
    else:
        # train
        prior, condprob, vocab = train(twenty_train)

        # saved train data in files
        with open('prior.pkl', 'wb') as data_file:
            pickle.dump(prior, data_file)
        with open('condprob.pkl', 'wb') as data_file:
            pickle.dump(condprob, data_file)
        with open('vocab.pkl', 'wb') as data_file:
            pickle.dump(vocab, data_file)

    end_time = datetime.datetime.now()
    print('End time - training', end_time)
    print('Training took', (end_time - start_time).total_seconds())

    twenty_test = fetch_20newsgroups(subset='test', shuffle=True,
                                     # categories=['alt.atheism', 'sci.space', 'talk.politics.guns', 'rec.autos']
                                     )

    n_correct = 0
    for doc_idx, doc in enumerate(twenty_test.data):
        doc_class = twenty_test.target[doc_idx]
        if predict(doc, prior, condprob, vocab) == doc_class:
            n_correct += 1
        # print(doc_idx, n_correct)

    print('Predicted %d correctly out of %d. Accuracy: %f' %
          (n_correct, len(twenty_test.data), float(n_correct / len(twenty_test.data)) * 100) + '%')


if __name__ == '__main__':
    main()
