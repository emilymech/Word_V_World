import pickle
from collections import Counter
from pathlib import Path

from ludwig.client import Client

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

combined_ww2cf = Counter()
project_name = Path.cwd().name
client = Client(project_name, param2default)
for param_path, label in client.gen_param_ps(param2requests, verbose=False):

    print(param_path)

    # get partial co-occurrence counts
    pkl_paths = list(param_path.glob('**/ww2cf.pkl'))  # TODO talk to me if this no longer works for new jobs
    if len(pkl_paths) == 0:
        raise FileNotFoundError(f'Did not find ww2cf.pkl in {param_path}')
    pkl_path = pkl_paths[0]
    ww2cf = pickle.load(pkl_path.open('rb'))

    # accumulate co-occurrence counts (across multiple jobs)
    partial_ww2cf = Counter(ww2cf)
    combined_ww2cf.update(partial_ww2cf)
    # print(combined_ww2cf)

    # to save memory, delete current iteration partial memory
    del partial_ww2cf

# save combined ww2cf to pkl file
combined_ww2cf_path = config.LocalDirs.root / 'data' / 'combined_ww2cf.pkl'
pickle.dump(combined_ww2cf, open(combined_ww2cf_path, 'wb'))



