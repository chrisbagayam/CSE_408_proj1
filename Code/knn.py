import sklearn
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

import pandas as pd
import string
from os import listdir
from os.path import isfile, join
from sklearn.preprocessing import MinMaxScaler

#Getting the list of text files
neg_mypath="../Data/kNN/training/neg"
neg_files = [f for f in listdir(neg_mypath) if isfile(join(neg_mypath, f))]

#Getting the list of text files
pos_mypath="../Data/kNN/training/pos"
pos_files = [f for f in listdir(pos_mypath) if isfile(join(pos_mypath, f))]
#print(pos_files)

# //////////Testing data////////////
#Getting the list of text files
test_neg_mypath="../Data/kNN/testing/neg"
test_neg_files = [f for f in listdir(test_neg_mypath) if isfile(join(test_neg_mypath, f))]

#Getting the list of text files
test_pos_mypath="../Data/kNN/testing/pos"
test_pos_files = [f for f in listdir(test_pos_mypath) if isfile(join(test_pos_mypath, f))]


df = pd.DataFrame()

def file_to_arr(path, files):
    #Positive 
    pos_total_arr = []
    for filname in files:
        f = open(path+"/"+filname, "r")
        no_punctuation = f.read().translate(str.maketrans('', '', string.punctuation))
        no_punctuation = no_punctuation.replace('\n','')
        pos_total_arr.append(no_punctuation.split(" "))
    # print(len(pos_total_arr))
        

    #Removing stopwords for #positive files
    no_s_word_arr = []
    sw = set(stopwords.words("english"))
    for i in pos_total_arr:
        no_s_word_arr.append([x for x in i if x not in sw and x!=""])
    return no_s_word_arr
#Removing stopwords for neg words

#Positive
#Bag of words
no_stop_word_arr = file_to_arr(pos_mypath, pos_files)
set_of_unique_words = {}
set_of_columns = set()
bag_of_word = []
for i in no_stop_word_arr:
    for word in i:
        set_of_columns.add(word)
        if word in set_of_unique_words:

            set_of_unique_words[word] = set_of_unique_words.get(word)+1
        else:
            set_of_unique_words[word] = 1
    set_of_unique_words["pos"] = 1
    bag_of_word.append(set_of_unique_words)
    set_of_unique_words = {}




#Negative
#Bag of words
neg_no_stop_word_arr = file_to_arr(neg_mypath,neg_files)
set_of_unique_words = {}
neg_set_of_columns = set()
for i in neg_no_stop_word_arr:
    for word in i:
        neg_set_of_columns.add(word)
        if word in set_of_unique_words:

            set_of_unique_words[word] = set_of_unique_words.get(word)+1
        else:
            set_of_unique_words[word] = 1
    set_of_unique_words["pos"] = 0
    bag_of_word.append(set_of_unique_words)
    set_of_unique_words = {}

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
    set_of_unique_words["pos"] = 0
    test_bag_of_word.append(set_of_unique_words)
    set_of_unique_words = {}


# dummy = []
# for i in range():
#     dummy.append(i)
# # test_bag_of_word.append(dummy)
# print(len(test_bag_of_word))



    # //////////////////////////////////////////////////////////


#Create a dataFrame for the test set ready to be used in the KNN model
df = pd.DataFrame(bag_of_word).fillna(0)
test_df = pd.DataFrame(test_bag_of_word).fillna(0)
scaler1 = MinMaxScaler()
scaler2 = MinMaxScaler()
scaled_data = scaler1.fit_transform(df)
test_scaled_data = scaler1.fit_transform(test_df)
df = pd.DataFrame(scaled_data,index=df.index,columns=df.columns)
test_df = pd.DataFrame(test_scaled_data,index=test_df.index,columns=test_df.columns)

#Reshaping test df
missing_columns = [x for x in df.columns if x not in test_df.columns]

for i in missing_columns:
    if(len(test_df.columns)!=len(df.columns)):
        test_df[i]=0
    else:
        break
# print(len(test_df))

# Constructing the KNN Module

#Separating x and y axis for training
X_train = df.drop(["pos"], axis=1)
y_train = df.pos



#Separating x and y axis for testing
X_test = test_df.drop(["pos"], axis=1)
y_test = test_df.pos

# X_test.fillna(0)
# print(X_test)
## Necessary imports for the classifier.
from sklearn.neighbors import KNeighborsClassifier
max_accuracy = 0
max_k=0
for k in range(1,25): 
    knn = KNeighborsClassifier(n_neighbors=k)
    # Fit the model on the training data.
    knn.fit(X_train, y_train)
    # Inspect how the model perform on test data
    score = knn.score(X_test, y_test)
    
    if(score > max_accuracy):
        max_accuracy = score
        max_k = k
print(max_accuracy * 100 , "% when k=", max_k )    
