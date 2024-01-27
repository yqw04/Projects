import string

# List of "unimportant" words (feel free to add more)
skip_words = ['a', 'about', 'all', 'an', 'another', 'any', 'around', 'at',
              'bad', 'beautiful', 'been', 'better', 'big', 'can', 'every', 'for',
              'from', 'good', 'have', 'her', 'here', 'hers', 'his', 'how',
              'i', 'if', 'in', 'into', 'is', 'it', 'its', 'large', 'later',
              'like', 'little', 'main', 'me', 'mine', 'more', 'my', 'now',
              'of', 'off', 'oh', 'on', 'please', 'small', 'some', 'soon',
              'that', 'the', 'then', 'this', 'those', 'through', 'till', 'to',
              'towards', 'until', 'us', 'want', 'we', 'what', 'when', 'why',
              'wish', 'with', 'would']

punctuation = ["!", ".", "/", "'", "`", "@", "^", "*", ",", "?"]


def filter_words(words, skip_words):
    new_list = []

    for elements in words:
        found = False
        for word in skip_words:
            if elements == word:
                found = True
        if found == False:
            new_list.append(elements)

    return new_list

    
def remove_punct(text):
    no_punct = ""
    for char in text:
        if not (char in punctuation):
            no_punct = no_punct + char

    return no_punct


def normalise_input(user_input):
    # Remove punctuation and convert to lower case
    no_punct = remove_punct(user_input).lower()
    sentence = no_punct.strip()
    new_list = sentence.split()
    return filter_words(new_list,skip_words)




    #
    # COMPLETE ME!
    #

