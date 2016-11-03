from InvertedIndex import get_inverted_index

def single_keyword_query():
    query = raw_input("Enter a single keyword search query: ")
    inverted_index = get_inverted_index("index_unfiltered")
    if inverted_index.has_key(query):
        for match in inverted_index[query]:
            print "Document with keyword: %s" % str(match)

def multiple_and_keyword_query():
    query = raw_input("Enter a multiple AND search query: ")
    matches = []
    inverted_index = get_inverted_index("index_unfiltered")
    for term in query.split():
        if inverted_index.has_key(term):
            if not matches:
                matches = inverted_index[term]
            else:
                matches = list(set(matches) & set(inverted_index[term]))
    for match in matches:
        print "Documents with keyword: %s" % str(match)

def multiple_or_keyword_query():
    query = raw_input("Enter a multiple OR search query: ")
    matches = []
    inverted_index = get_inverted_index("index_unfiltered")
    for term in query.split():
        if inverted_index.has_key(term):
            matches = matches + inverted_index[term]
    matches = [(doc, matches.count(doc)) for doc in set(matches)]
    matches = sorted(matches, key=lambda tup:tup[1], reverse=True)
    for tuple in matches:
        print "Documents with keyword: %s Occurrences: %s" % (tuple[0], tuple[1])

single_keyword_query()
multiple_and_keyword_query()
multiple_or_keyword_query()

