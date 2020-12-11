
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk import pos_tag
import itertools
import os

# have bag of words only be verbs and adjectives
#create a big ole bag of words, but a lot of fluff even when we remove stop words,
#so make feature vectors the 1000 most common in each bag of words for pos and neg

movie_reviews = []
#index 0 - neg movie reviews
#index 1 - pos movie reviews

neg_revies_most_common_words = []
neg_reviews_feature_vector = []

pos_revies_most_common_words = []
pos_reviews_feature_vector = pos_revies_most_common_words[:1000]

pos_reviews_bag_of_words = []
neg_reviews_bag_of_words = []

threshold = 10

dirs = ["text_data/neg","text_data/pos"]
for dir in dirs:
    cur_list = []
    for file in os.listdir(dir):
        cur_list.append(file)
    movie_reviews.append(cur_list)

stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
             "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her",
             "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs",
             "themselves", "what", "which", "who", "whom", "this", "that", "these",
             "those", "am", "is", "are", "was", "were", "be", "been", "being", "have",
             "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and",
             "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for",
             "with", "about", "against", "between", "into", "through", "during", "before",
             "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
             "over", "under", "again", "further", "then", "once", "here", "there", "when", "where",
             "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
             "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can",
             "will", "just", "don", "should", "now","much","many","first","last","big","little"]

symbols = [".",":",",",";","?","!","&","$","(",")","@","#","%","^","-","/","+","-","`","~",
           "[","]","{","}","'\'","<",">","'","\"","``","'s","n't","_","*","v'e","'ve","I'm","'m"]

#parse through pos movie reviews and tokenize each one
neg_movie_reviews = movie_reviews[0]
for i in range(len(neg_movie_reviews)):
    cur_review = open("text_data/neg/" + neg_movie_reviews[i],'r').read()
    acceptable_pos = ['JJ']
    cur_review_word_tokenized = word_tokenize(cur_review)
    filtered_list = [word for word in cur_review_word_tokenized if word not in stopwords
    and word not in symbols]

    filtered_list_tagged = pos_tag(filtered_list)
    filtered_list_pos = []
    for i in range(len(filtered_list_tagged)):
        if filtered_list_tagged[i][1] in acceptable_pos:
            filtered_list_pos.append(filtered_list_tagged[i][0])

    neg_reviews_bag_of_words.append(filtered_list_pos)

fdist_neg = FreqDist(itertools.chain.from_iterable(neg_reviews_bag_of_words))
for i in range(len(fdist_neg.most_common())):
    word = fdist_neg.most_common()[i][0]
    frequency = fdist_neg.most_common()[i][1]
    if frequency >= threshold:
        neg_revies_most_common_words.append(tuple((word,frequency)))

neg_reviews_feature_vector = neg_revies_most_common_words[:1000]
f_nfv = open("neg_fv.txt",'w')
for word_frequency_pair in neg_reviews_feature_vector:
    f_nfv.write(word_frequency_pair[0] + "," + str(word_frequency_pair[1]) + "\n")




pos_movie_reviews = movie_reviews[1]
for i in range(len(pos_movie_reviews)):
    cur_review = open("text_data/pos/" + pos_movie_reviews[i],'r').read()
    acceptable_pos = ['JJ']
    cur_review_word_tokenized = word_tokenize(cur_review)
    filtered_list = [word for word in cur_review_word_tokenized if word not in stopwords
    and word not in symbols]

    filtered_list_tagged = pos_tag(filtered_list)
    filtered_list_pos = []
    for i in range(len(filtered_list_tagged)):
        if filtered_list_tagged[i][1] in acceptable_pos:
            filtered_list_pos.append(filtered_list_tagged[i][0])

    pos_reviews_bag_of_words.append(filtered_list_pos)

fdist_pos = FreqDist(itertools.chain.from_iterable(pos_reviews_bag_of_words))
for i in range(len(fdist_pos.most_common())):
    word = fdist_pos.most_common()[i][0]
    frequency = fdist_pos.most_common()[i][1]
    if frequency >= threshold:
        pos_revies_most_common_words.append(tuple((word,frequency)))

pos_reviews_feature_vector = pos_revies_most_common_words[:1000]
f_pfv = open("pos_fv.txt",'w')
for word_frequency_pair in pos_reviews_feature_vector:
    f_pfv.write(word_frequency_pair[0] + "," + str(word_frequency_pair[1]) + "\n")

