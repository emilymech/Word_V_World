import pickle
from pathlib import Path
from scipy import sparse
from sortedcontainers import SortedSet

from word_v_world.cooc_matrix import make_sparse_ww_matrix
from word_v_world.tokenization import gen_tokenized_articles
from word_v_world.articles import get_text_file_path


def main(param2val):  # param2val appears auto-magically via Ludwig
    cwc_param_name = param2val['cwc_param_name']
    window_size = param2val['window_size']
    window_weight = param2val['window_weight']
    window_type = param2val['window_type']
    vocab_name = param2val['vocab_name']
    article_coverage = param2val['article_coverage']
    # added by Ludwig
    project_path = Path(param2val['project_path'])
    save_path = Path(param2val['save_path'])  # all data that is saved must be saved here

    for k, v in param2val.items():
        print(k, v)

    # step 0
    print('Making vocab...')
    vocab_path = project_path / 'data' / '{}.txt'.format(vocab_name)
    if not vocab_path.exists():
        raise FileNotFoundError('{} not found on server'.format(vocab_path))
    vocab = SortedSet(vocab_path.read_text().split('\n'))
    vocab.discard('')  # not sure why empty string is in vocab - but it is
    assert len(vocab) > 0

    print('Loaded {} words from vocab'.format(len(vocab)))

    # step 1
    print('Tokenizing...', flush=True)
    param_path = project_path.parent / 'CreateWikiCorpus' / 'runs' / cwc_param_name
    bodies_path = get_text_file_path(param_path, 'bodies')
    titles_path = get_text_file_path(param_path, 'titles')
    num_docs = len(titles_path.read_text().split('\n')) - 1  # "wc -l" says there is 1 less line
    print(f'Number of articles in text file={num_docs}')
    tokenized_docs = gen_tokenized_articles(bodies_path, num_docs)  # this also lower-cases

    # step 2
    print('Making co-occurrence matrix', flush=True)
    w2id = {w: n for n, w in enumerate(vocab)}  # python 3 integers have dynamic size
    id2w = {n: w for n, w in enumerate(vocab)}
    max_num_docs = int(num_docs * article_coverage)
    cooc_matrix = make_sparse_ww_matrix(tokenized_docs,
                                        w2id,
                                        max_num_docs=max_num_docs,
                                        window_size=window_size,
                                        window_type=window_type,
                                        window_weight=window_weight,
                                        )
    verbose = True if cooc_matrix.size < 1000 else False
    ids2cf = sparse.dok_matrix(cooc_matrix).todok()
    ww2cf = {}
    print('Converting sparse matrix to dictionary...', flush=True)
    for ids, cf in ids2cf.items():
        i1, i2 = ids
        word1 = id2w[i1]
        word2 = id2w[i2]
        ww = (word1, word2)
        ww2cf[ww] = cf
    # check
    if verbose:
        print(w2id)
        print(cooc_matrix.toarray())
        print(cooc_matrix.shape)
        print(ww2cf)

    # step 3 - save the dictionary containing co-occurrence frequencies to Ludwig-supplied save_path
    print('Saving dictionary to disk...')
    ww2cf_path = save_path / 'ww2cf.pkl'
    if not ww2cf_path.parent.exists():
        ww2cf_path.parent.mkdir(parents=True)
    pickle.dump(ww2cf, ww2cf_path.open('wb'))

    print("Emily is done making a wiki co-occurrence dictionary! Wait for the folders to finish moving!")

    return []
