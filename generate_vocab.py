from word_v_world.word_count import make_master_w2f
from datetime import datetime

from word_v_world import config

VOCAB_SIZE = 10000000  # using this to use all of wiki
NUM_LUDWIG_WORKERS = 6
W2DF_FILE_NAME = 'w2dfs_4800000_ALL.pkl'


def main():
    wiki_param_names = ['param_{}'.format(22 + i) for i in range(NUM_LUDWIG_WORKERS)]

    master_w2f = make_master_w2f(wiki_param_names, W2DF_FILE_NAME)

    sorted_master_vocab = (w for w, f in master_w2f.most_common())  # returns all words, most frequent first

    # save word and frequency pair to file
    wf_pairs = 'wf_allwiki_' + datetime.now().strftime('%Y%m%d_%H-%M-%S')
    with (config.Dirs.root / 'data' / '{}.txt'.format(wf_pairs)).open('w') as file:
        for w, f in master_w2f.items():
            file.write(str(w) + ', ' + str(f) + '\n')

    # # sort
    # vocab = set()
    # while len(vocab) < VOCAB_SIZE:
    #     w: str = next(sorted_master_vocab)
    #
    #     # filter words
    #     if w.isnumeric():
    #         continue
    #     if len(w) == 1:
    #         continue
    #
    #     vocab.add(w)
    #
    # # create unique vocab identifier
    # vocab_name = "_vocab_"
    # event_id = str(VOCAB_SIZE) + vocab_name + datetime.now().strftime('%Y%m%d_%H-%M-%S')
    #
    # # save to file
    # with (config.Dirs.root / 'data' / '{}.txt'.format(event_id)).open('w') as f:
    #     for n, w in enumerate(vocab):
    #         f.write(w + '\n')
    #
    # return sorted_master_vocab


if __name__ == '__main__':
    main()
