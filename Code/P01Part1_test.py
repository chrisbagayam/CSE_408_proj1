from datetime import datetime
t = datetime.now()
import sklearn
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from math import sqrt
import pandas as pd
import string
from os import listdir
from os.path import isfile, join
from sklearn.preprocessing import MinMaxScaler
from cse408_knn import *

# //////////Testing data////////////
#Getting the list of text files
test_neg_mypath="../Data/kNN/testing/neg"
test_neg_files = [f for f in listdir(test_neg_mypath) if isfile(join(test_neg_mypath, f))]

#Getting the list of text files
test_pos_mypath="../Data/kNN/testing/pos"
test_pos_files = [f for f in listdir(test_pos_mypath) if isfile(join(test_pos_mypath, f))]


# ///////////////////////////////////////////////////////////////////////////////////
# Importing Test Data

#Positive
#Bag of words
test_no_stop_word_arr = file_to_arr(test_pos_mypath,test_pos_files)
set_of_unique_words = {}
set_of_columns = set()
test_bag_of_word = []
for i in test_no_stop_word_arr:
    for word in i:
        set_of_columns.add(word)
        if word in set_of_unique_words:

            set_of_unique_words[word] = set_of_unique_words.get(word)+1
        else:
            set_of_unique_words[word] = 1
    

    #removing low frequency words
    for key in list(set_of_unique_words):
        if(set_of_unique_words[key] <5):
            set_of_unique_words.pop(key)
    

    set_of_unique_words["pos"] = 1

    test_bag_of_word.append(set_of_unique_words)
    set_of_unique_words = {}
# print(len(test_bag_of_word))


#Negative
#Bag of words
test_neg_no_stop_word_arr = file_to_arr(test_neg_mypath,test_neg_files)
set_of_unique_words = {}
neg_set_of_columns = set()
for i in test_neg_no_stop_word_arr:
    for word in i:
        neg_set_of_columns.add(word)
        if word in set_of_unique_words:

            set_of_unique_words[word] = set_of_unique_words.get(word)+1
        else:
            set_of_unique_words[word] = 1
    
    
    #Removing low frequency words
    for key in list(set_of_unique_words):
        if(set_of_unique_words[key] <5):
            set_of_unique_words.pop(key)

    
    set_of_unique_words["pos"] = 0

    test_bag_of_word.append(set_of_unique_words)
    set_of_unique_words = {}

# ///////////////////////////////////////////////////////////////////////////////
test_df = pd.DataFrame(test_bag_of_word).fillna(0)

def get_accuracy(pred, actual):
    acc = 0
    for idx in range(len(pred)):
        if(pred[idx] == actual[idx]):
            acc = acc +1
    acc = acc / len(pred)
    print(acc*100, "%"+" accuracy")

# uncomment the following to run each distance metric

#SSD
# vec = cse408_knn(test_df, 5, 1)

#Angular
# vec = cse408_knn(test_df, 5, 2)

#Common words
vec = cse408_knn(test_df, 5, 3)
# print(vec)
get_accuracy(vec, test_df.pos)



