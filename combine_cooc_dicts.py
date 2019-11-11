import pickle
from collections import Counter
from pathlib import Path

from ludwig.results import gen_param_paths

from word_v_world import config
from word_v_world.params import param2requests, param2default

# TODO - save combined_dict to different folder within data for each config

# specify which parameter configuration for which to retrieve results
update_dict = {
    'cwc_param_name': ['param_22', 'param_23', 'param_24', 'param_25', 'param_26', 'param_27'],
    'num_machines': [6],
    'vocab_name': ['100000_vocab_20191108_15-17-19'],
    'article_coverage': [0.5]
}
param2requests.update(update_dict)

# get paths from which to load co-occurrence data
combined_ww2cf = Counter()
project_name = Path.cwd().name
paths_to_ww2cf = []
for param_path, label in gen_param_paths(project_name,
                                         param2requests,
                                         param2default,
                                         research_data_path=config.LocalDirs.research_data,
                                         verbose=True):
    pkl_paths = list(param_path.glob('**/saves/ww2cf.pkl'))
    if len(pkl_paths) == 0:
        raise FileNotFoundError(f'Did not find ww2cf.pkl in {param_path}')
    else:
        print(f'Found {pkl_paths[0]}')
    paths_to_ww2cf.append(pkl_paths[0])

# accumulate co-occurrence counts (across multiple jobs)
for path_to_ww2cf in paths_to_ww2cf:
    ww2cf = pickle.load(path_to_ww2cf.open('rb'))
    partial_ww2cf = Counter(ww2cf)
    combined_ww2cf.update(partial_ww2cf)
    del partial_ww2cf

# save combined ww2cf to pkl file
combined_ww2cf_path = config.LocalDirs.data / 'combined_ww2cf.pkl'
pickle.dump(combined_ww2cf, open(combined_ww2cf_path, 'wb'))



