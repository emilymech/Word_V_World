from word_v_world.word_count import make_master_w2f
from datetime import datetime

from word_v_world import config

NUM_LUDWIG_WORKERS = 6

"""
this script is still good to have, in case you want to compute word counts outside of the context
of computing pmi. in case, someone asks you for word counts, for example.
"""


def main():

    # count all words
    # note: counting should use the same tokenizer used everywhere else in the project
    wiki_param_names = ['param_{}'.format(22 + i) for i in range(NUM_LUDWIG_WORKERS)]
    master_w2f = make_master_w2f(wiki_param_names)

    # save word and frequency pair to file
    wf_pairs = 'wf_allwiki_' + datetime.now().strftime('%Y%m%d_%H-%M-%S')
    with (config.Dirs.root / 'data' / '{}.txt'.format(wf_pairs)).open('w') as file:
        for w, f in sorted(master_w2f.items(), key=lambda i: i[1], reverse=True):
            file.write(str(w) + ' ' + str(f) + '\n')


if __name__ == '__main__':
    main()
