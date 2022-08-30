import numpy as np
from scipy import sparse
from typing import Generator, Set, List, Dict, Optional
from cytoolz import itertoolz
from itertools import chain
from itertools import islice

# TODO - initialize the matrix to be the same size so the transpose works


def make_sparse_ww_matrix(docs: Generator[List[str], None, None],
                          w2id: Dict[str, int],
                          window_size: int,
                          window_type: str,
                          window_weight: str,
                          max_num_docs: Optional[int] = None,
                          pad='*PAD*',
                          ) -> sparse.coo_matrix:

    print('Counting word-word co-occurrences in {}-word moving window'.format(window_size))

    # init lists for sparse matrix construction
    rows = []
    cols = []
    data = []

    if max_num_docs is not None:
        docs = islice(docs, max_num_docs)

    print(len(w2id))

    for tokens in docs:
        # pad tokens such that all co-occurrences in last window are captured
        padding = (pad for _ in range(window_size))
        tokens_padded = chain(tokens, padding)

        # + 1 because window consists of w2s only
        for window in itertoolz.sliding_window(window_size + 1, tokens_padded):

            for w1, w2, dist in zip([window[0]] * window_size, window[1:],
                                    range(window_size)):
                if w1 in w2id and w2 in w2id:

                    w1_id = w2id[w1]
                    w2_id = w2id[w2]
                    rows.append(w1_id)
                    cols.append(w2_id)
                    # increment
                    if w1_id == pad or w2_id == pad:
                        continue
                    if window_weight == "linear":
                        data.append(window_size - dist)
                    elif window_weight == "flat":
                        data.append(1)

    matrix = sparse.coo_matrix((np.array(data, dtype=np.int32), (rows, cols)))

    # window_type
    if window_type == 'forward':
        matrix = matrix
    elif window_type == 'backward':
        matrix = matrix.transpose()
    elif window_type == 'summed':
        matrix = matrix + matrix.transpose()
    elif window_type == 'concatenated':
        matrix = np.concatenate((matrix, matrix.transpose()), axis=1)
    else:
        raise AttributeError('Invalid arg to "window_type".')
    print('Shape of matrix={}'.format(matrix.shape))

    return matrix



