# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 17:14:55 2021

@author: Lwax Malax
"""
import buildVoc
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize

# function to return text as an array
def feat_vec(filepath,voc):
    # initial array of the text file given in the path
    text_arr = []
    # frequency of each word in the lexicon (voc)
    frequency = 0
    # the one-dimensional feature vector 
    feat_vec = []
    # getting the vocabulary array
    voc = buildVoc.buildVoc()
    # Open the file with read only permit
    f = open(filepath,'r')
    # use readline() to read the first line 
    line = f.readline()
    text_arr.append(line)
    while line:
        # use realine() to read next line
        line = f.readline()
        text_arr.append(line)
       
    f.close()
    # converting array of words to a string in lower case
    str1 = " "   
    list_as_a_string = str1.join(text_arr).lower()

    # Tokenizing the string
    # This returns a list of tokens
    text_tokens = word_tokenize(list_as_a_string)    

    for word in voc: 
        frequency = text_tokens.count(word)
        feat_vec.append(frequency)
    #print(feat_vec)
    return feat_vec



