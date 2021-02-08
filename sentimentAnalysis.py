# Sentiment Analysis

from string import digits
import string

import os


def main():
    absolute_path = os.path.abspath('Data/SA/neg')

    for filename in os.listdir(absolute_path):
            print (filename)#+ "\t"+ str(sentimentAnalysis(absolute_path + "/"+ filename)))
    absolute_path = os.path.abspath('Data/SA/pos')

    for filename in os.listdir(absolute_path):
            print (filename)#+ "\t"+ str(sentimentAnalysis(absolute_path + "/"+ filename)))


def sentimentAnalysis(filename):
    path = 'Data/SA/wordWithStrength.txt' #file path will need to be changed
    f = open(path, 'r')
    lexicon = f.read().splitlines()
    #print(lexicon)

    numbers = lexicon

    indexs = remove_numbers(lexicon)
    scores = remove_words(numbers)

    file = open(filename, 'r')
    txt_set = file.read()
    return get_text_score(txt_set, indexs, scores)


def get_text_score(txt_set, indexs, scores):
    total_score = 0

    words_in_file = []

    #null_chars will not be counted in words or be used to split words
    null_chars = [',', '.', '?', '!', ';', ':', ')', '(', '/', '\"', '$', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    #word_split consists of avery char that will be used to split up words
    word_split = [' ', '-', '\'', '_', '\n', '\t']

    stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "re"]

    word = ""
    for char in txt_set:
        if char in null_chars:
            continue
        elif char in word_split:
            if word not in stopwords and len(word) > 1:
                index = get_word_score(word, indexs)

                if index != -1:
                    total_score += float(scores[index])

            word = ""

        else:
            word += char
    return total_score



def get_word_score(word, indexs):
    if word in indexs:
        return indexs.index(word)
    else:
        return -1





# create array with only the words
def remove_numbers(lexicon):
    remove_digits = str.maketrans('', '', digits)
    removeTab = str.maketrans('', '', ".-\t")
    lexicon = [i.translate(remove_digits) for i in lexicon]
    lexicon = [i.translate(removeTab) for i in lexicon]
    return lexicon

#print(remove(lexicon))

#create array with only the sentiment score numbers
def remove_words(numbers):
    new_numbers = []
    place_of_tab = 0
    for num in numbers:
        for index in range(len(num)):
            if num[index] == "\t":
                place_of_tab = index
        new_numbers.append(num[place_of_tab+1:len(num)])



    return new_numbers

#print(remove(numbers))




if __name__ == "__main__":
    main()
