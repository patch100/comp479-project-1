import glob
import os
import cPickle
import TextNormalizer
import BM25

from bs4 import BeautifulSoup
from Inverter import spimi_invert


def process_documents(block_size, normalizer_method, index_file):
    path = 'reuters21578/*.sgm'
    #path = 'reuters21578/reut2-000.sgm'

    # path for each reuters file
    files = glob.glob(path)

    block_files = []

    N = 0
    doc_length_dict = {}
    # loop through each file
    for file in files:

        # parse each document separately
        soup = BeautifulSoup(open(file), 'html.parser')
        documents = soup.find_all('reuters')
        N += len(documents)
        tokens = []

        # loop through all the documents
        for doc in documents:

            # tokenize each document
            if doc.body is not None and doc.body.text is not None:
                text = doc.body.text
                doc_id = int(doc['newid'].encode("utf-8"))
                doc_length_dict[doc_id] = len(text.split())
                tokens = tokens + normalizer_method(text, doc_id)

        block_files = block_files + spimi_invert(tokens, block_size)

    save_collection_stats(N, doc_length_dict)

    build_inverted_index(block_files, index_file)

    BM25.RankDocuments(index_file, get_inverted_index(index_file))


def save_collection_stats(N, doc_length_dict):
    total_docs_length = 0
    for key, value in doc_length_dict.items():
        total_docs_length += value
    avg_doc_length = total_docs_length / N
    with open("collection_stats", "wb") as stats_file:
        cPickle.dump((N, doc_length_dict, avg_doc_length), stats_file, protocol=cPickle.HIGHEST_PROTOCOL)
    stats_file.close()


def build_inverted_index(block_files, index_file):
    for block_file in block_files:
        merge_blocks(block_file, index_file)


def get_inverted_index(index_file):
    with open(index_file, 'rb') as load_file:
        inverted_index = cPickle.load(load_file)
    load_file.close()
    inverted_index = dict(inverted_index)
    return dict(inverted_index)


def merge_blocks(block_path, index_file):
    inverted_index = {}

    with open(block_path, 'rb') as block_file:
        block = cPickle.load(block_file)
    block_file.close()

    if os.path.isfile(index_file):
        with open(index_file, 'rb') as output_file:
            index = cPickle.load(output_file)
        output_file.close()

        for dictionary in [index, block]:
            for key, value in dictionary.iteritems():
                inverted_index.setdefault(key, []).extend(value)
    else:
        inverted_index = block

    with open(index_file, "wb") as output_file:
        cPickle.dump(inverted_index, output_file, protocol=cPickle.HIGHEST_PROTOCOL)
    output_file.close()
    os.remove(block_path)


def print_info():
    # files = ["index_unfiltered", "index_no_numbers", "index_case_folding", "index_30_stop_words", "index_150_stop_words", "index_stemming"]
    files = ["index_unfiltered"]
    for file_name in files:
        inverted_index = get_inverted_index(file_name)
        count = sum(len(post) for post in inverted_index.itervalues())

        with open("collection_stats", 'rb') as stats_files:
            N, doc_length_dict, avg_doc_length = cPickle.load(stats_files)
        stats_files.close()

        print "Stats for " + file_name
        print "Number of distinct terms: " + str(len(inverted_index))
        print "Number of tokens: " + str(count)
        print "Number of documents processed: " + str(N)
        print "Average document length: " + str(avg_doc_length) + " words"


# process_documents(1024, TextNormalizer.unfiltered, "index_unfiltered")
# process_documents(1024, TextNormalizer.no_numbers, "index_no_numbers")
# process_documents(1024, TextNormalizer.case_folding, "index_case_folding")
# process_documents(1024, TextNormalizer.thirty_stop_words, "index_30_stop_words")
# process_documents(1024, TextNormalizer.one_hundred_fifty_stop_words, "index_150_stop_words")
# process_documents(1024, TextNormalizer.stemming, "index_stemming")

print_info()
