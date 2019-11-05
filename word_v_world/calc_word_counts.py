import pickle
from pathlib import Path

from word_v_world import config


# get the pickle for each param folder individually
def get_pickles(wiki_param_name, w2dfs_file_name):
    research_data = Path('/Volumes') / 'research_data'
    remote_root = research_data / 'CreateWikiCorpus'
    wiki_param_path = remote_root / 'runs' / wiki_param_name
    if not wiki_param_path.exists():
        raise FileNotFoundError('{} does not exist'.format(wiki_param_path))
    full_path = wiki_param_path / w2dfs_file_name
    with full_path.open('rb') as file:
        w2dfs = pickle.load(file)
    return w2dfs  # this is a list of dicts by article in params


def make_dict_lowercase(dict):
    dict_lower = {k.lower(): v for k, v in dict.items()}
    return dict_lower


# loop over each individual pickle and add unique keys to dictionaries/update values of non-unique keys
def make_master_dict(wiki_param_name, file_name):
    master_dict = {}
    for param in wiki_param_name:
        print("Adding {}".format(param))
        current_w2dfs = get_pickles(param, file_name)
        for current_dict in current_w2dfs:

            lower_dict = make_dict_lowercase(current_dict)
            for key in lower_dict:
                if key in master_dict:
                    master_dict[key] += lower_dict[key]
                else:
                    master_dict[key] = lower_dict[key]
                # print("New size is {}".format(len(master_dict)))
    return master_dict







