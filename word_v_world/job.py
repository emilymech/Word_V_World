import pickle
from pathlib import Path
from scipy import sparse

from word_v_world import config
from word_v_world.cooc_matrix import CoocMatrix
from word_v_world.tokenization import tokenize


def main(param2val):  # param2val appears auto-magically via Ludwig

    cwc_param_name = param2val['cwc_param_name']
    window_size = param2val['window_size']
    window_weight = param2val['window_weight']
    window_type = param2val['window_type']
    # added by Ludwig
    project_path = Path(param2val['project_path'])
    save_path = Path(param2val['save_path'])  # all data that is saved must be saved here

    for k, v in param2val.items():
        print(k, v)

    # step 0
    print('Making vocab...')
    vocab_path = project_path / 'data' / 'vocab.txt'
    if not vocab_path.exists():
        raise FileNotFoundError('{} not found on server'.format(vocab_path))
    vocab = set(vocab_path.read_text().split('\n'))
    assert len(vocab) > 10

    if config.Global.debug:
        vocab = {'the', 'on', 'you', 'i'}

    print('Loaded {} words from vocab'.format(len(vocab)))

    # step 1
    print('Tokenizing...', flush=True)
    param_path = project_path.parent / 'CreateWikiCorpus' / 'runs' / cwc_param_name
    path_to_articles = list(param_path.glob('**/bodies.txt'))
    if len(path_to_articles) == 0:
        raise SystemExit('Did not find bodies.txt in {}'.format(param_path))

    all_tokens = tokenize(path_to_articles)

    # step 2
    print('Making co-occurrence matrix', flush=True)
    the_cooc_matrix = CoocMatrix(window_size=window_size,
                                 window_weight=window_weight,
                                 window_type=window_type,
                                 vocab=vocab)
    the_cooc_matrix.update_from_list(all_tokens)
    print('Done updating')
    if config.Global.debug:
        print(the_cooc_matrix.cooc_matrix.toarray())
        print(the_cooc_matrix.cooc_matrix.shape)

    ids2cf = sparse.dok_matrix(the_cooc_matrix.cooc_matrix).todok()
    ww2cf = {}
    print('Converting sparse matrix to dictionary...', flush=True)
    for ids, cf in ids2cf.items():
        i1, i2 = ids
        word1 = the_cooc_matrix.id2w[i1]
        word2 = the_cooc_matrix.id2w[i2]
        ww = (word1, word2)
        ww2cf[ww] = cf
        print(ww, cf)

    # step 3 - save the dictionary containing co-occurrence frequencies to Ludwig-supplied save_path
    ww2cf_path = save_path / 'ww2cf.pkl'
    if not ww2cf_path.parent.exists():
        ww2cf_path.parent.mkdir(parents=True)
    pickle.dump(ww2cf, ww2cf_path.open('wb'))

    print("All done! :)")

    return []
