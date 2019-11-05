import spacy

from word_v_world import config
from word_v_world.cooc_matrix import CoocMatrix
from word_v_world.tokenization import tokenize


def main(param2val):  # param2val appears auto-magically via Ludwig

    param_name = param2val['param_name']
    window_size = param2val['window_size']
    window_weight = param2val['window_weight']
    window_type = param2val['window_type']

    # step 0
    print('Making vocab...')
    vocab_path = config.RemoteDirs.root / 'data' / 'vocab.txt'  # TODO make sure this is uploaded
    if not vocab_path.exists():
        raise FileNotFoundError('{} not found on server'.format(vocab_path))
    vocab = vocab_path.read_text().split('\n')

    print(vocab)
    assert len(vocab) > 10

    # step 1
    print('Tokenizing...')
    param_path = config.RemoteDirs.runs / param_name
    path_to_article = list(param_path.glob('**/bodies.txt'))[0]
    paths_to_articles = [path_to_article]
    all_tokens = tokenize(paths_to_articles)

    # step 2
    print('Making co-occurrence matrix')
    the_cooc_matrix = CoocMatrix(window_size=window_size,
                                 window_weight=window_weight,
                                 window_type=window_type,
                                 vocab=vocab)
    the_cooc_matrix.update_from_list(all_tokens)
    ids2cf = the_cooc_matrix.cooc_matrix.todok()
    ww2cf = {}
    for ids, cf in ids2cf.items():
        i1, i2 = ids
        word1 = the_cooc_matrix.id2w[i1]
        word2 = the_cooc_matrix.id2w[i2]
        ww = (word1, word2)
        ww2cf[ww] = cf
        print(ww, cf)

        raise SystemExit('Debugging')

    # step 3 - save the dictionary containing co-occurrence frequencies

    return []