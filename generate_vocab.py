from word_v_world.word_count import make_master_dict

from word_v_world import config


def main():
    wiki_param_name = ['param_{}'.format(22 + i) for i in range(num_ludwig_workers)]

    w2f = make_master_dict(wiki_param_name, file_name)

    # sort
    vocab = sorted(w2f.keys(), key=lambda w: w2f[w], reverse=True)

    # save to file
    with (config.LocalDirs.root / 'data' / 'vocab.txt').open('w') as f:
        for w in vocab:
            f.write(w + '\n')


if __name__ == '__main__':
    num_ludwig_workers = 6
    file_name = 'w2dfs_4800000_ALL.pkl'
    main()