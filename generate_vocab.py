from word_v_world.word_count import make_master_w2f
from datetime import datetime

from word_v_world import config

VOCAB_SIZE = 100000
NUM_LUDWIG_WORKERS = 6
W2DF_FILE_NAME = 'w2dfs_4800000_ALL.pkl'


def main():
    wiki_param_names = ['param_{}'.format(22 + i) for i in range(NUM_LUDWIG_WORKERS)]

    w2f = make_master_w2f(wiki_param_names, W2DF_FILE_NAME, VOCAB_SIZE)

    # sort
    vocab = sorted(w2f.keys(), key=lambda w: w2f[w], reverse=True)

    # create unique vocab identifier
    vocab_name = "_vocab_"
    event_id = str(VOCAB_SIZE) + vocab_name + datetime.now().strftime('%Y%m%d_%H-%M-%S')

    # save to file
    with (config.LocalDirs.root / 'data' / '{}.txt'.format(event_id)).open('w') as f:
        for n, w in enumerate(vocab):
            if n == VOCAB_SIZE:
                break
            f.write(w + '\n')


if __name__ == '__main__':
    main()
