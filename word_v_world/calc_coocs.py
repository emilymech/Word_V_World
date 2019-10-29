import numpy as np
import sys
import pyprind


from cytoolz import itertoolz


# TODO: write the function to get the files loaded in

class CoocMatrix:

    def __init__(self):
        self.corpus_name = None
        self.corpus_file_list = None

        self.window_size = None
        self.window_weight = None
        self.window_type = None

        self.num_documents = 0
        self.corpus_path = None
        self.document_list = []

        self.num_words = None
        self.word_list = None
        self.word_index_dict = None

        self.pad = '*PAD*'
        self.verbose = False

        self.cooc_matrix = None

    def init_ww_matrix(self, window_size, window_weight, window_type, word_list_file):
        self.window_size = window_size
        self.window_weight = window_weight
        self.window_type = window_type
        self.cooc_matrix = np.zeros([self.num_words, self.num_words], int)

        self.word_list = []
        self.word_index_dict = {}
        self.num_words = 0

        f = open(word_list_file)
        for line in f:
            word = line.strip().strip('\n').strip()
            self.word_list.append(word)
            self.word_index_dict[word] = self.num_words
            self.num_words += 1

    def get_file_list(self, path_to_corpora):
        pass
        # create a list of the paths to all the param/bodies.txt files
        # save that as self.corpus_file_list

    def add_documents_to_matrix(self):
        for i in range(len(self.corpus_file_list)):
            filename = self.corpus_file_list[i]
            f = open(filename)
            for line in f:
                tokens = (line.strip().strip('\n').strip()).split()
                self.add_to_ww_matrix_fast(tokens)

    def add_to_ww_matrix_fast(self, tokens):  # no function call overhead - twice as fast


        pbar = pyprind.ProgBar(self.num_documents, stream=sys.stdout)

        print('\nCounting word-word co-occurrences in {}-word moving window'.format(self.window_size))

        tokens += [self.pad] * self.window_size  # add padding such that all co-occurrences in last window are captured
        if self.verbose:
            print(tokens)
        windows = itertoolz.sliding_window(self.window_size + 1, tokens)  # + 1 because window consists of t2s only

        for w in windows:

            for t1, t2, dist in zip([w[0]] * self.window_size, w[1:], range(self.window_size)):
                if t1 in self.word_index_dict and t2 in self.word_index_dict:

                    t1_id = self.word_index_dict[t1]
                    t2_id = self.word_index_dict[t2]
                # increment
                    if t1_id == self.pad or t2_id == self.pad:
                        continue
                    if self.window_weight == "linear":
                        self.cooc_matrix[t1_id, t2_id] += self.window_size - dist
                    elif self.window_weight == "flat":
                        self.cooc_matrix[t1_id, t2_id] += 1
                    if self.verbose:
                        print('row {:>3} col {:>3} set to {}'.format(t1_id, t2_id, self.cooc_matrix[t1_id, t2_id]))

        if self.verbose:
            print()
        pbar.update()
        # window_type
        if self.window_type == 'forward':
            self.cooc_matrix = self.cooc_matrix
        elif self.window_type == 'backward':
            self.cooc_matrix = self.cooc_matrix.transpose()
        elif self.window_type == 'summed':
            self.cooc_matrix = self.cooc_matrix + self.cooc_matrix.transpose()
        elif self.window_type == 'concatenated':
            self.cooc_matrix = np.concatenate((self.cooc_matrix, self.cooc_matrix.transpose()), axis=1)
        else:
            raise AttributeError('Invalid arg to "window_type".')
        print('Shape of normalized matrix={}'.format(self.cooc_matrix.shape))


def main():
    window_size = 1
    window_weight = 'flat'
    window_type = 'forward'
    word_list_file = 'file_location.txt'
    path_to_corpora = 'path'

    the_cooc_matrix = CoocMatrix()
    the_cooc_matrix.init_ww_matrix(window_size, window_weight, window_type, word_list_file)
    the_cooc_matrix.get_file_list(path_to_corpora)
    the_cooc_matrix.add_documents_to_matrix()


main()
