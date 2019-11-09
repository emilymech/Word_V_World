import unittest
import numpy as np
from word_v_world.cooc_matrix import make_sparse_ww_matrix


class MyTest(unittest.TestCase):

    @staticmethod
    def test1():

        tokenized_docs = (doc for doc in ['w1 w2 w3 w4 w5 w6 w7 w1 w2 w3 w4 w5 w6 w7 w1 w2 w3 w4 w5 w6 w7'.split(),
                                          'w1 w2 w3 w4 w5 w6 w7 w1 w2 w3 w4 w5 w6 w7'.split(),
                                          'w1 w2 w3 w4 w5 w6 w7'.split()])
        w2id = {'w1': 0, 'w2': 1, 'w3': 2, 'w4': 3, 'w5': 4, 'w6': 5, 'w7': 6}

        cooc_matrix = make_sparse_ww_matrix(tokenized_docs,
                                            w2id,
                                            window_size=2,
                                            window_type='forward',
                                            window_weight='flat',
                                            )
        res = cooc_matrix.toarray()

        gold = [
            [0, 6, 6, 0, 0, 0, 0],
            [0, 0, 6, 6, 0, 0, 0],
            [0, 0, 0, 6, 6, 0, 0],
            [0, 0, 0, 0, 6, 6, 0],
            [0, 0, 0, 0, 0, 6, 6],
            [3, 0, 0, 0, 0, 0, 6],
            [3, 3, 0, 0, 0, 0, 0],
        ]

        return np.array_equal(res, gold)


if __name__ == '__main__':
    unittest.main()
