import numpy as np
from scipy import sparse

from cytoolz import itertoolz


class CoocMatrix:

    def __init__(self, window_size, window_weight, window_type, vocab):
        self.corpus_name = None
        self.corpus_file_list = None

        self.window_size = window_size
        self.window_weight = window_weight
        self.window_type = window_type

        self.num_words = 0
        self.word_list = []
        self.w2id = {}
        self.id2w = {}

        self.pad = '*PAD*'
        self.verbose = False

        self.cooc_matrix = None

        for word in vocab:
            self.word_list.append(word)
            self.w2id[word] = self.num_words
            self.id2w[self.num_words] = word
            self.num_words += 1

        assert self.num_words > 0

    def update_from_list(self, tokens):
        self.add_to_ww_matrix_fast(tokens)

    def add_to_ww_matrix_fast(self, tokens):  # no function call overhead - twice as fast

            print('\nCounting word-word co-occurrences in {}-word moving window'.format(self.window_size))

            rows = []
            cols = []
            data = []

            tokens += [self.pad] * self.window_size  # add padding such that all co-occurrences in last window are captured
            windows = itertoolz.sliding_window(self.window_size + 1, tokens)  # + 1 because window consists of t2s only

            for w in windows:

                for t1, t2, dist in zip([w[0]] * self.window_size, w[1:], range(self.window_size)):
                    if t1 in self.w2id and t2 in self.w2id:

                        t1_id = self.w2id[t1]
                        t2_id = self.w2id[t2]
                        rows.append(t1_id)
                        cols.append(t2_id)
                        # increment
                        if t1_id == self.pad or t2_id == self.pad:
                            continue
                        if self.window_weight == "linear":
                            data.append(self.window_size - dist)
                        elif self.window_weight == "flat":
                            data.append(1)

            self.cooc_matrix = sparse.coo_matrix((np.array(data), (np.array(rows), np.array(cols))), dtype=np.int64)

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



