import nltk
import random
from nltk.corpus import movie_reviews
import pickle

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



