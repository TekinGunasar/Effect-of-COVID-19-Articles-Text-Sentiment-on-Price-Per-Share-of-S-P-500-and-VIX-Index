import nltk
import random
import pickle
from nltk.classify.scikitlearn import SklearnClassifier

from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import LinearSVC,NuSVC

import os

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


article_summaries = [file for file in os.listdir("covid_articles_summaries")]
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

classifiers = [pickle.load(open("classifiers/"+classifier,"rb"))
               for classifier in os.listdir("classifiers")]

voted_classifier = VoteClassifier(classifiers[0],classifiers[1],classifiers[2],classifiers[3],classifiers[4])


print("Classification:",voted_classifier.classify(testing_set[0][0]),"Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
print("Classification:",voted_classifier.classify(testing_set[1][0]),"Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
print("Classification:",voted_classifier.classify(testing_set[2][0]),"Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
print("Classification:",voted_classifier.classify(testing_set[3][0]),"Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
print("Classification:",voted_classifier.classify(testing_set[4][0]),"Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
print("Classification:",voted_classifier.classify(testing_set[5][0]),"Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)

