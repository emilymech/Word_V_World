from collections import Counter
from typing import List
from timeit import default_timer as timer
from pathos.pools import ProcessPool
from itertools import islice

from word_v_world import config
from word_v_world.tokenization import tokenizer

NUM_WORKERS = 4
NUM_TEXTS_PER_PROCESS = 1000


def make_w2dfs(texts: List[str],
               ) -> Counter:
    print('Starting worker')
    start = timer()
    w2param_f = Counter()
    num_processed = 0
    for doc in tokenizer.pipe(texts):

        words = [w.lower_ for w in doc]   # this performs lower-casing before counting

        w2param_f.update(words)
        num_processed += 1

    print(f'Took {timer() - start:.4f} secs to count words in {num_processed} docs', flush=True)
    return w2param_f


def make_master_w2f(wiki_param_names: List[str],
                    ) -> Counter:

    res = Counter()
    for wiki_param_name in wiki_param_names:

        # load text file
        remote_root = config.Dirs.research_data / 'CreateWikiCorpus'
        wiki_param_path = remote_root / 'runs' / wiki_param_name
        print(f'Reading bodies.txt in {wiki_param_path}')
        path_to_articles = list(wiki_param_path.glob('**/bodies.txt'))[0]

        line_reader = islice(path_to_articles.open('r'), 8000)
        texts = [doc for doc in zip(*(line_reader,) * NUM_TEXTS_PER_PROCESS)]
        num_texts = len(texts)
        print('Number of text chunks: {}'.format(num_texts))

        # count in multiple processes
        pool = ProcessPool(NUM_WORKERS)
        w2_param_f_list = pool.map(make_w2dfs, texts)

        # add to master
        print("Adding word counts from {} to master_w2f".format(wiki_param_name))
        for w2param_f in w2_param_f_list:
            res.update(w2param_f)

    print(f'Length of master_w2f={len(res)}')
    return res







