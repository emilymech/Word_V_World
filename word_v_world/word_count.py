import pickle
from pathlib import Path
from collections import Counter
from typing import List, Dict


# get the pickle for each param folder individually
def gen_w2dfs(wiki_param_name: str,
              w2dfs_file_name: str):
    research_data = Path('/Volumes') / 'research_data'
    remote_root = research_data / 'CreateWikiCorpus'
    wiki_param_path = remote_root / 'runs' / wiki_param_name
    if not wiki_param_path.exists():
        raise FileNotFoundError('{} does not exist'.format(wiki_param_path))
    full_path = wiki_param_path / w2dfs_file_name
    with full_path.open('rb') as file:
        w2dfs = pickle.load(file)
    for w2df in w2dfs:  # this is a list of dicts by article in params
        yield w2df


def make_master_w2f(wiki_param_names: List[str],
                    file_name: str,
                    size: int,
                    ) -> Dict[str, int]:
    print('Making master_w2f')
    res = Counter()
    for param in wiki_param_names:
        print("Adding {}".format(param))
        for w2df in gen_w2dfs(param, file_name):

            # TODO exclude single letter words + numeric types ....

            res.update(w2df)
    print(f'Done. Length={len(res)}')
    return dict(res.most_common(size))







