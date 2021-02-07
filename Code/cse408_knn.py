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
from sklearn.metrics.pairwise import cosine_similarity

#Getting the list of text files
neg_mypath="../Data/kNN/training/neg"
neg_files = [f for f in listdir(neg_mypath) if isfile(join(neg_mypath, f))]

#Getting the list of text files
pos_mypath="../Data/kNN/training/pos"
pos_files = [f for f in listdir(pos_mypath) if isfile(join(pos_mypath, f))]
#print(pos_files)



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
    
    #Removing low frequency words
    for key in list(set_of_unique_words):
        if(set_of_unique_words[key] <5):
            set_of_unique_words.pop(key)

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
    
    #Removing low frequency words
    for key in list(set_of_unique_words):
        if(set_of_unique_words[key] <5):
            set_of_unique_words.pop(key)

    set_of_unique_words["pos"] = 0
    bag_of_word.append(set_of_unique_words)
    set_of_unique_words = {}


def cse408_knn(test_df, k, DstType):
    
    #Create a dataFrame for the test set ready to be used in the KNN model
    df = pd.DataFrame(bag_of_word).fillna(0)
    scaler1 = MinMaxScaler()
    scaler2 = MinMaxScaler()
    scaled_data = scaler1.fit_transform(df)
    test_scaled_data = scaler1.fit_transform(test_df)
    df = pd.DataFrame(scaled_data,index=df.index,columns=df.columns)
    test_df = pd.DataFrame(test_scaled_data,index=test_df.index,columns=test_df.columns)

    # print(df.shape)
    # print(test_df.shape)
    #Reshaping test df
    missing_columns = [x for x in df.columns if x not in test_df.columns]

    for i in missing_columns:
        if(len(test_df.columns)!=len(df.columns)):
            test_df[i]=0
        else:
            break
    
    y_test = test_df.pos
    
    print("please wait...")

    if(DstType==3):
        return word_in_com_distance(k, df, test_df, y_test)
    if(DstType==2):
        return dist_cos(k, df, test_df, y_test)
    elif(DstType==1):
        return ssd(k, df, test_df, y_test)



# Cosine distance
def dist_cos(k, df, test_df, y_test ):
    cos_distances=[]
    for t_index, t_row in test_df.iterrows():
        # arr = [[cosine_similarity([t_row], [row])[0][0], row["pos"]] 
        #         for index, row in df.iterrows()]
        arr = []
        for index, row in df.iterrows():
            sum_a = 0
            sum_b = 0
            sum_top = 0
            for col_name, val in row.iteritems():
                sum_a += t_row.get(col_name, default=0) * t_row.get(col_name, default=0)
                sum_b += row.get(col_name, default=0) * row.get(col_name, default=0)
                sum_top += t_row.get(col_name, default=0) * row.get(col_name, default=0)

            if(sum_a != 0 and sum_b != 0):    
                cos_similarity = sum_top / ((sqrt(sum_a)) * (sqrt(sum_b)))
            arr.append([cos_similarity, row["pos"]])
            
        arr = sorted(arr, key=lambda x: x[0], reverse=True)
        arr = arr[:k]
        # cos_distances.append(arr)

        pos_count = 0
        neg_count = 0
        for i in arr:
            if int(i[1])==1:
                pos_count = pos_count+1
            else:
                neg_count = neg_count+1
        
        if pos_count >= neg_count:
            cos_distances.append(1)
        else:
            cos_distances.append(0)        

    return cos_distances
# dist_cos(5)
# print(type(row))




#  Words in common
def word_in_com_distance(k, df, test_df, y_test):
    wic_distance = []
    for t_index, t_row in test_df.iterrows():
        arr = []
        for index, row in df.iterrows():
            words_in_common = 0
            category = row["pos"]

            for col_name, val in row.iteritems():
                if t_row.get(col_name)!=0 and row.get(col_name):
                    words_in_common=words_in_common+1
                # break
            arr.append([words_in_common, category])
            # break

        arr = sorted(arr, key=lambda x: x[0], reverse=True)
        arr = arr[:k]

        #dominating label
        pos_count = 0
        neg_count = 0
        for i in arr:
            if int(i[1])==1:
                pos_count = pos_count+1
            else:
                neg_count = neg_count+1
        
        if pos_count >= neg_count:
            wic_distance.append(1)
        else:
            wic_distance.append(0)
    
    return wic_distance


#SSD
def ssd(k, df, test_df, y_test):
    ssd_distance = []
    for t_index, t_row in test_df.iterrows():
        arr = []
        for index, row in df.iterrows():
            sum_sq = 0
            for col_name, val in row.iteritems():
                sum_sq = sum_sq+ (t_row.get(col_name, default=0)-row.get(col_name, default=0))**2
                # print(sum_sq)
                # break

            arr.append([sum_sq, row["pos"]])
            # break

        arr = sorted(arr, key=lambda x: x[0], reverse=False)
        arr = arr[:k]

         #dominating label
        pos_count = 0
        neg_count = 0
        for i in arr:
            if int(i[1])==1:
                pos_count = pos_count+1
            else:
                neg_count = neg_count+1
        
        if pos_count >= neg_count:
           ssd_distance.append(1)
        else:
            ssd_distance.append(0)
        # ssd_distance.append(arr)
        # break
    return ssd_distance

# ssd(5)
# word_in_com_distance(21)
# print(datetime.now() - t, "seconds")