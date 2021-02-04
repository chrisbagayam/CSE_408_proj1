import os

def buildVoc(folder, vocabulary):
    data_set = get_txt_from_folder(folder)
    vocabulary = get_vocabulary(data_set, vocabulary)

    return vocabulary


#get_vocabulary(data_set, vocabulary) will split the data set into words and add it to the vocabulary
def get_vocabulary(data_set, vocabulary):

    frequency = []

    #null_chars will not be counted in words or be used to split words
    null_chars = [',', '.', '?', '!', ';', ':', ')', '(', '/', '\"', '$', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    #word_split consists of avery char that will be used to split up words
    word_split = [' ', '-', '\'', '_', '\n', '\t']

    stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "re"]

    word = ""
    for char in data_set:
        if char in null_chars:
            continue
        elif char in word_split:
            if word not in vocabulary and word not in stopwords and len(word) > 1:
                vocabulary.append(word)
            if word in vocabulary:
                if len(frequency) <= vocabulary.index(word):
                    frequency.append(1)
                else:
                    frequency[vocabulary.index(word)] += 1
            word = ""
        else:
            word += char

    vocabulary = remove_low_frequencies(vocabulary, frequency, 6)

    return vocabulary


def remove_low_frequencies(vocabulary, frequency, threshold):
    new_vocabulary = []

    for i in range(0, len(vocabulary)):
        if frequency[i] >= threshold:
            new_vocabulary.append(vocabulary[i])

    return new_vocabulary


#get_txt_from_folder(folder) will go though every file in the folder and get the text
def get_txt_from_folder(folder):

    file_txt = ""
    absolute_path = os.path.abspath(folder)


    for filename in os.listdir(absolute_path):
            file = open(absolute_path + "/"+ filename, 'r')

            file_txt += file.read()
            file.close()
    return file_txt
