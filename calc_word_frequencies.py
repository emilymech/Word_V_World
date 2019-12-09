from word_v_world.word_count import make_master_w2f
from datetime import datetime

from word_v_world import config

NUM_LUDWIG_WORKERS = 6

"""
ph made some changes here dec 9, 2019.

the problem is that the wdf pickle files were created by counting words after processing
wiki articles with the default spacy tokenizer - which splits on contractions and hyphens.
however, all your work does not assume this kind of tokenization.
the solution was to count words using your own tokenizer, and not rely on loading in the w2df pickle files.
"""


def main():

    # count all words
    # note: counting should use the same tokenizer used everywhere else in the project
    wiki_param_names = ['param_{}'.format(22 + i) for i in range(NUM_LUDWIG_WORKERS)]
    master_w2f = make_master_w2f(wiki_param_names)

    # save word and frequency pair to file
    wf_pairs = 'wf_allwiki_' + datetime.now().strftime('%Y%m%d_%H-%M-%S')
    with (config.Dirs.root / 'data' / '{}.txt'.format(wf_pairs)).open('w') as file:
        for w, f in master_w2f.items():
            file.write(str(w) + ' ' + str(f) + '\n')


if __name__ == '__main__':
    main()
