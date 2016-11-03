from nltk.stem import PorterStemmer
from string import punctuation

def unfiltered(text, id):
    return token_tuples(text.split(), id)

def no_numbers(text, id):
    text = remove_numbers(text)
    return token_tuples(text.split(), id)

def case_folding(text, id):
    text = remove_numbers(text)
    tokens = tokenize(text)
    return token_tuples(tokens, id)

def thirty_stop_words(text, id):
    text = remove_numbers(text)
    tokens = tokenize(text)
    tokens = remove_stop_words_30(tokens)
    return token_tuples(tokens, id)

def one_hundred_fifty_stop_words(text, id):
    text = remove_numbers(text)
    tokens = tokenize(text)
    tokens = remove_stop_words_150(tokens)
    return token_tuples(tokens, id)

def stemming(text, id):
    text = remove_numbers(text)
    tokens = tokenize(text)
    tokens = remove_stop_words_150(tokens)
    tokens = stem_tokens(tokens)
    return token_tuples(tokens, id)

def remove_numbers(text): return ''.join([word for word in text if not word.isdigit()])

def clean_tokens(tokens):
    return [token.translate(token.maketrans("",""), punctuation) for token in tokens]

def tokenize(text):
    text = text.lower()
    return text.split()

def remove_stop_words_150(tokens): return [token for token in tokens if token not in stopwords150]

def remove_stop_words_30(tokens): return [token for token in tokens if token not in stopwords30]

def stem_tokens(tokens):
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]

def token_tuples(tokens, id) : return [(token.encode("utf-8"), id) for token in tokens]

stopwords150 = ["a","about","above","after","again","against","all","am","an","and","any","are","as","at","be","because","been","before","being","below","between","both","but","by","can","cannot","could","did","do","does","doing","don't","down","during","each","few","for","from","further","had","has","have","haven't","having","he","he's","her","here","hers","herself","him","himself","his","hot","how","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","my","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","reuter","same","she","should","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","where","which","while","who","whom","why","with","won't","would","wouldn't","you","you're","your","yours","yourself"]
stopwords30 = ["i","a","about","an","and","are","as","at","be","by","for","from","has","in","is","it","of","on","that","the","this","to","was","were","what","when","where","who","will","with"]