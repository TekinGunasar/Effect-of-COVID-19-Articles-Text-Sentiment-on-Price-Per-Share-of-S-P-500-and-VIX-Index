import nltk
import random
from nltk.corpus import movie_reviews
import pickle
from nltk.classify.scikitlearn import SklearnClassifier

from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import LinearSVC,NuSVC

from nltk.classify import ClassifierI
from statistics import mode

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

documents = []

for category in movie_reviews.categories():
    for fileid in movie_reviews.fileids(category):
        documents.append(list((movie_reviews.words(fileid),category)))

random.shuffle(documents)

all_words = []
for w in movie_reviews.words():
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:3000]

def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(rev),category) for (rev,category) in documents]

training_set = featuresets[:1900]
testing_set = featuresets[1900:]

classifier_f = open("naivebayes.pickle","rb")
classifier = pickle.load(classifier_f)
classifier_f.close()

print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier,testing_set))*100)
classifier.show_most_informative_features(15)

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

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier Algo accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier,testing_set))*100)

voted_classifier = VoteClassifier(classifier,MNB_classifier,BernoulliNB_classifier,LogisticRegression_classifier,SGD_classifier,LinearSVC_classifier,NuSVC_classifier)
print("voted_classifier accurcay percent:",nltk.classify.accuracy(voted_classifier,testing_set)*100)

print("Classification:",voted_classifier.classify(testing_set[0][0]),"Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)

