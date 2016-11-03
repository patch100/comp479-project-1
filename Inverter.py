import cPickle
import sys
import uuid

def spimi_invert(token_stream, block_size):
    dictionary = {}
    output_files = []
    for token in token_stream:
        if (sys.getsizeof(dictionary) / 1024) < block_size:
            dictionary = add_to_dictionary(token, dictionary)
        else:
            output_files = output_files + [write_block_to_disk(dictionary)]
            dictionary.clear()
            dictionary = add_to_dictionary(token, dictionary)

    output_files = output_files + [write_block_to_disk(dictionary)]
    return output_files


def add_to_dictionary(token, dictionary):
    if dictionary.has_key(token[0]):
        if token[1] not in dictionary[token[0]]:
            dictionary[token[0]].append(token[1])
    else:
        dictionary[token[0]] = [token[1]]
    return dictionary


def write_block_to_disk(dictionary):
    with open(str(uuid.uuid4()), "wb") as output_file:
        cPickle.dump(dictionary, output_file, protocol=cPickle.HIGHEST_PROTOCOL)
    output_file.close()
    return output_file.name