

def sentimentAnalysis(filename):
    indexs = []
    scores = []

    file = open(filename, 'r')
    txt_set = file.read()
    get_text_score(txt_set, indexs, scores)

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
                #add scores here
                score = get_word_score(word, indexs, scores)
                if score != null:
                    total_score += score

            word = ""
        else:
            word += char



def get_word_score(word, indexs, scores):
    index = indexs.find(word)
    if index != -1:
        return scores[index]
    else:
        return null

if __name__ == "__main__":
    main()
