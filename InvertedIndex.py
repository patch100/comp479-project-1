import glob
import os
import cPickle

from bs4 import BeautifulSoup

import TextNormalizer
from Inverter import spimi_invert


def process_documents(block_size, normalizer_method, index_file):
    path = 'reuters21578/*.sgm'
    #path = 'reuters21578/reut2-000.sgm'

    # path for each reuters file
    files=glob.glob(path)

    block_files = []

    # loop through each file
    for file in files:

        # parse each document separately
        soup = BeautifulSoup(open(file), 'html.parser')
        documents = soup.find_all('reuters')
        tokens = []

        # loop through all the documents
        for doc in documents:

            # tokenize each document
            if doc.body is not None and doc.body.text is not None:
                text = doc.body.text
                tokens = tokens + normalizer_method(text, doc['newid'].encode("utf-8"))

        block_files = block_files + spimi_invert(tokens, block_size)

    build_inverted_index(block_files, index_file)

def build_inverted_index(block_files, index_file):
    for block_file in block_files:
        merge_blocks(block_file, index_file)

    with open(index_file, 'rb') as load_file:
        inverted_index = cPickle.load(load_file)
    load_file.close()
    return inverted_index

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

# process_documents(500, TextNormalizer.unfiltered, "index_unfiltered")
# process_documents(500, TextNormalizer.no_numbers, "index_no_numbers")
# process_documents(500, TextNormalizer.case_folding, "index_case_folding")
# process_documents(500, TextNormalizer.thirty_stop_words, "index_30_stop_words")
# process_documents(500, TextNormalizer.one_hundred_fifty_stop_words, "index_150_stop_words")
# process_documents(1024, TextNormalizer.stemming, "index_stemming")

def print_info():
    for file_name in ["index_unfiltered", "index_no_numbers", "index_case_folding", "index_30_stop_words", "index_150_stop_words", "index_stemming"]:
        inverted_index = get_inverted_index(file_name)
        count = sum(len(post) for post in inverted_index.itervalues())
        print "Stats for " + file_name
        print "Number of distinct terms: " + str(len(inverted_index))
        print "Number of tokens: " + str(count)

print_info()
