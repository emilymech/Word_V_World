from collections import Counter
from typing import List
from timeit import default_timer as timer
from pathos.pools import ProcessPool

from word_v_world import config
from word_v_world.tokenization import tokenizer

NUM_LUDWIG_WORKERS = 6


def count_words_in_text_file(wiki_param_name: str,
                             ) -> Counter:
    print('Starting worker')

    # get path
    remote_root = config.Dirs.research_data / 'CreateWikiCorpus'
    wiki_param_path = remote_root / 'runs' / wiki_param_name
    print(f'Reading bodies.txt in {wiki_param_path}')
    path_to_articles = list(wiki_param_path.glob('**/bodies.txt'))[0]

    # load text file
    line_reader = path_to_articles.open('r')

    # count
    start = timer()
    w2param_f = Counter()
    num_processed = 0
    for doc in tokenizer.pipe(line_reader):
        words = [w.lower_ for w in doc]   # this performs lower-casing before counting
        w2param_f.update(words)
        num_processed += 1

        # if num_processed % 1000 == 0:
            # print(num_processed)

    print(f'Took {timer() - start:.4f} secs to count words in {num_processed} docs', flush=True)
    return w2param_f


def make_master_w2f(wiki_param_names: List[str],
                    ) -> Counter:

    # count in multiple processes
    num_wiki_param_names = len(wiki_param_names)
    print('Starting process pool')
    pool = ProcessPool(num_wiki_param_names)
    w2_param_f_list = pool.map(count_words_in_text_file, wiki_param_names)
    print('Done collecting counts')

    # add to master
    res = Counter()
    print('Aggregating counts')
    for w2param_f in w2_param_f_list:
        res.update(w2param_f)

    print(f'Length of master_w2f={len(res)}')
    return res


def get_word_freq():
    # count all words
    # note: counting should use the same tokenizer used everywhere else in the project
    wiki_param_names = ['param_{}'.format(22 + i) for i in range(NUM_LUDWIG_WORKERS)]
    master_w2f = make_master_w2f(wiki_param_names)
    return master_w2f


def get_total_token_count(master_w2f):
    total_words_in_wiki = sum([master_w2f[k] for k in master_w2f])
    print(total_words_in_wiki)
    return total_words_in_wiki
