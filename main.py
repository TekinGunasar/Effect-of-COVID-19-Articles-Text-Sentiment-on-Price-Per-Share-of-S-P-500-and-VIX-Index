import nltk
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB,MultinomialNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from nltk.classify import ClassifierI
from statistics import mode
import pickle

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

acceptable_pos = ['J']
documents = []

all_words = []

for sent in pos.split('\n'):
    documents.append((sent,"pos"))
    words = word_tokenize(sent)
    pos = nltk.pos_tag(words)
    for word in pos:
        if word[1][0] in acceptable_pos:
            all_words.append(word[0].lower())

for sent in neg.split('\n'):
    documents.append((sent,"neg"))
    words = word_tokenize(sent)
    pos = nltk.pos_tag(words)
    for word in pos:
        if word[1][0] in acceptable_pos:
            all_words.append(word[0].lower())

pos_words = word_tokenize(pos)
neg_words = word_tokenize(neg)

for w in pos_words:
    all_words.append(w.lower())

for w in neg_words:
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:5000]

def find_features(text):
    words = word_tokenize(text)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(sent),category) for (sent,category) in documents]

training_set = featuresets[:10000]
testing_set = featuresets[10000:]

NB_classifier = nltk.NaiveBayesClassifier.train(training_set)
print("NB:", (nltk.classify.accuracy(NB_classifier,testing_set))*100)
save_NB = open("classifiers/" + "nb.pickle","wb")
pickle.dump(NB_classifier,save_NB)
save_NB.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB:", (nltk.classify.accuracy(MNB_classifier,testing_set))*100)
save_MNB = open("classifiers/" + "mnb.pickle")
pickle.dump(MNB_classifier,save_MNB)
save_MNB.close()

BNB_classifier = SklearnClassifier.train(BernoulliNB())
BNB_classifier.train(training_set)
print("BNB:", (nltk.classify.accuracy(BNB_classifier,testing_set))*100)
save_BNB = open("classifiers/" + "bnb.pickle")
pickle.dump(BNB_classifier,save_BNB)
save_BNB.close()

LR_classifier = SklearnClassifier(LogisticRegression())
LR_classifier.train(training_set)
print("LR:", (nltk.classify.accuracy(LR_classifier,testing_set))*100)
save_LR = open("classifiers/" + "lr.pickle")
pickle.dump(LR_classifier,save_LR)
save_LR.close()


SGD_classifier = SklearnClassifier(SGDClassifier)
SGD_classifier.train(training_set)
print("SGD:", (nltk.classify.accuracy(SGD_classifier,testing_set))*100)
save_SGD = open("classifiers/" + "sgd.pickle")
pickle.dump(SGD_classifier,save_SGD)
save_SGD.close()


