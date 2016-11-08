import cPickle
import operator
from math import log10

def GetRankedResults(query, inverted_index):

    matches = {}

    with open("collection_stats", 'rb') as stats_files:
        N, doc_length_dict, avg_doc_length = cPickle.load(stats_files)
    stats_files.close()

    N = float(N)

    for term in query.split():
        if inverted_index.has_key(term):
            dft = float(len(inverted_index[term]))
            for posting in inverted_index[term]:
                if matches.has_key(posting[0]):
                    rsvd = ((posting[2] * (log10((N/dft)))) + matches[posting[0]])
                else:
                    rsvd = (posting[2] * (log10((N/dft))))
                matches[posting[0]] = rsvd

    return sorted(matches.items(), key=operator.itemgetter(1), reverse=True)

def RankDocuments(index_file, inverted_index):
    # Book page 233
    # "In the absence of such optimization, experiments have shown
    # reasonable values are to set k1 and k3 to
    # a value between 1.2 and 2 and b = 0.75."
    k1 = 1.5
    b = 0.5

    # fetch collection stats
    with open("collection_stats", 'rb') as stats_files:
        N, doc_length_dict, avg_doc_length = cPickle.load(stats_files)
    stats_files.close()

    doc_length_dict = dict(doc_length_dict)

    for term, postings in inverted_index.items():
        for index, post in enumerate(postings):
            tftd = post[1]
            doc_id = post[0]
            ld = doc_length_dict[doc_id]
            inverted_index[term][index] = (post[0], post[1], calculate_rsv(avg_doc_length, b, k1, ld, tftd))

    with open(index_file, "wb") as output_file:
        cPickle.dump(inverted_index, output_file, protocol=cPickle.HIGHEST_PROTOCOL)
    output_file.close()


def calculate_rsv(avg_doc_length, b, k1, ld, tftd):
    avg_doc_length = float(avg_doc_length)
    b = float(b)
    k1 = float(k1)
    ld = float(ld)
    tftd = float(tftd)
    return float(((k1 + 1) * tftd) / (k1 * (((1 - b) + b * (ld / avg_doc_length))) + tftd))






