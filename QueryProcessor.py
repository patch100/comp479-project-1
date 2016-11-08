from BM25 import GetRankedResults
from InvertedIndex import get_inverted_index

index_file = "index_unfiltered"


def single_keyword_query():
    query = get_user_input("Enter a single keyword search query: ")
    inverted_index = get_inverted_index(index_file)
    if inverted_index.has_key(query):
        for match in inverted_index[query]:
            print "Document with keyword: %s" % str(match[0])


def multiple_and_keyword_query():
    query = get_user_input("Enter a multiple AND search query: ")
    matches = []
    inverted_index = get_inverted_index(index_file)
    for term in query.split():
        if inverted_index.has_key(term):
            if not matches:
                matches = inverted_index[term]
            else:
                matches = list(set(matches) & set(inverted_index[term]))
    for match in matches[:20]:
        print "Documents with keyword: %s" % str(match[0])


def multiple_or_keyword_query():
    query = get_user_input("Enter a multiple OR search query: ")
    matches = []
    inverted_index = get_inverted_index(index_file)
    for term in query.split():
        if inverted_index.has_key(term):
            matches = matches + inverted_index[term]
    matches = [(doc[0], matches.count(doc)) for doc in set(matches)]
    matches = sorted(matches, key=lambda tup: tup[1], reverse=True)
    for tuple in matches[:20]:
        print "Documents with keyword: %s Occurrences: %s" % (tuple[0], tuple[1])


def ranked_search():
    print "This query returns the top 20 results, using BM25 Ranking"
    query = get_user_input("Enter a search query: ")
    inverted_index = get_inverted_index(index_file)
    matches = GetRankedResults(query, inverted_index)
    for match in matches[:20]:
        print "Document ID: %s RSVd: %s" % (str(match[0]), str(match[1]))


def get_user_input(prompt):
    return raw_input(prompt)


# single_keyword_query()
# multiple_and_keyword_query()
# multiple_or_keyword_query()
ranked_search()
