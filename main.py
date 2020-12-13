import nltk
import random
import pickle
from nltk.classify.scikitlearn import SklearnClassifier

from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import LinearSVC,NuSVC

from nltk.classify import ClassifierI
from statistics import mode

from nltk.tokenize import word_tokenize

class VoteClassifier(ClassifierI):
    def __init__(self,*classifiers):
        self._classifiers = classifiers

    def classify(self,features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self,features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes/len(votes)
        return conf

pos = open("positive.txt",'r').read()
neg = open("negative.txt",'r').read()

documents = []

for sent in pos.split('\n'):
    documents.append((sent,"pos"))

for sent in neg.split('\n'):
    documents.append((sent,"neg"))

all_words = []
pos_words = word_tokenize(pos)
neg_words = word_tokenize(neg)

for w in pos_words:
    all_words.append(w.lower())

for w in neg_words:
    all_words.append(w.lower())


all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:5000]

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(sent),category) for (sent,category) in documents]

random.shuffle(featuresets)

training_set = featuresets[:10000]
testing_set = featuresets[10000:]

NB_classifier = nltk.NaiveBayesClassifier.train(testing_set)
print("NB_Classifier Algo accuracy percent:",(nltk.classify.accuracy(NB_classifier,testing_set))*100)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier Algo accuracy percent:", (nltk.classify.accuracy(MNB_classifier,testing_set))*100)

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier Algo accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier,testing_set))*100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier Algo accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier,testing_set))*100)

SGD_classifier = SklearnClassifier(SGDClassifier())
SGD_classifier.train(training_set)
print("SGD_classifier Algo accuracy percent:", (nltk.classify.accuracy(SGD_classifier,testing_set))*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier Algo accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier,testing_set))*100)

voted_classifier = VoteClassifier(NB_classifier,MNB_classifier,BernoulliNB_classifier,SGD_classifier,LinearSVC_classifier)
print("voted_classifier accurcay percent:",nltk.classify.accuracy(voted_classifier,testing_set)*100)

print("Classification:",voted_classifier.classify(testing_set[0][0]),"Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)

