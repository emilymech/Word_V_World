from word_v_world.word_count import make_master_dict
from datetime import datetime

from word_v_world import config

vocab_size = 100000


def main():
    wiki_param_name = ['param_{}'.format(22 + i) for i in range(num_ludwig_workers)]

    w2f = make_master_dict(wiki_param_name, file_name)

    # sort
    vocab = sorted(w2f.keys(), key=lambda w: w2f[w], reverse=True)

    # create unique vocab identifier
    vocab_name = "_vocab_"
    event_id = str(vocab_size) + vocab_name + datetime.now().strftime('%Y%m%d-%H:%M:%S')

    # save to file
    with (config.LocalDirs.root / 'data' / '{}.txt'.format(event_id)).open('w') as f:
        for n, w in enumerate(vocab):
            if n == vocab_size:
                break
            f.write(w + '\n')


if __name__ == '__main__':
    num_ludwig_workers = 6
    file_name = 'w2dfs_4800000_ALL.pkl'
    main()
