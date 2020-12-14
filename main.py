import nltk
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB,MultinomialNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from nltk.classify import ClassifierI
from statistics import mode
import os
import pickle
from pathlib import Path
import math

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

pos_labels = open("training_data/positive.txt",'r').read()
neg_labels = open("training_data/negative.txt",'r').read()

acceptable_pos = ['J']
documents = []

all_words = []

for sent in pos_labels.split('\n'):
    documents.append((sent,"pos"))
    words = word_tokenize(sent)
    pos = nltk.pos_tag(words)
    for word in pos:
        if word[1][0] in acceptable_pos:
            all_words.append(word[0].lower())

for sent in neg_labels.split('\n'):
    documents.append((sent,"neg"))
    words = word_tokenize(sent)
    pos = nltk.pos_tag(words)
    for word in pos:
        if word[1][0] in acceptable_pos:
            all_words.append(word[0].lower())

pos_words = word_tokenize(pos_labels)
neg_words = word_tokenize(neg_labels)

for w in pos_words:
    all_words.append(w.lower())

for w in neg_words:
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

word_features_f = open("word_features.pickle","rb")
word_features = pickle.load(word_features_f)
word_features_f.close()

def find_features(text):
    words = word_tokenize(text)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

classifiers = [pickle.load(open("classifiers/"+classifier,"rb"))
               for classifier in os.listdir("classifiers")]

classifier = VoteClassifier(classifiers[0],classifiers[1],classifiers[2],
                            classifiers[3],classifiers[4])

f = open("text_sentiment_per_day.txt",'w')
for file in os.listdir("covid_articles_summaries"):
    cur_summaries = open("covid_articles_summaries/" + file,'r').readlines()
    cur_date = Path('covid_articles_urls/' + file).stem.split(".")[0]
      
    cur_sum = 0
    for summary in cur_summaries:
        current_feature_vector = find_features(summary)
        if classifier.classify(current_feature_vector) == "pos":
            cur_sum += classifier.confidence(current_feature_vector)
        else:
            cur_sum -= classifier.confidence(current_feature_vector)
    sentiment = cur_sum/len(cur_summaries)

    f.write(cur_date + f" Sentiment: {sentiment:.2f}" + '\n')
    print(cur_date + f" Sentiment: {sentiment:.2f}" + '\n')


       
