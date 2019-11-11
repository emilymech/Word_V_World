import pickle
from collections import Counter
from typing import List, Dict

from word_v_world import config


# get the pickle for each param folder individually
def gen_w2dfs(wiki_param_name: str,
              w2dfs_file_name: str):
    remote_root = config.Dirs.research_data / 'CreateWikiCorpus'
    wiki_param_path = remote_root / 'runs' / wiki_param_name
    print(f'Path to w2dfs={wiki_param_path}')
    if not wiki_param_path.exists():
        raise FileNotFoundError('{} does not exist'.format(wiki_param_path))
    full_path = wiki_param_path / w2dfs_file_name

    print(f'Loading {full_path}')
    with full_path.open('rb') as file:
        w2dfs = pickle.load(file)
    print('Done')

    # yield word counts by document
    for w2df in w2dfs:
        yield w2df


def make_master_w2f(wiki_param_names: List[str],
                    file_name: str,
                    ) -> Counter:
    res = Counter()
    for wiki_param_name in wiki_param_names:
        print("Adding word counts from {} to master_w2f".format(wiki_param_name))
        for w2df in gen_w2dfs(wiki_param_name, file_name):
            res.update(w2df)

    print(f'Length of master_w2f={len(res)}')
    return res







