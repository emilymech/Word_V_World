import pickle
from collections import Counter

from ludwig.client import Client

from word_v_world import config
from word_v_world.params import param2requests, param2default


# specify which parameter configuration for which to retrieve results
update_dict = {
    'cwc_param_name': ['param_0', 'param_1'], # to sum over multiple, add the params in the list
    'num_machines': [1],
}
param2requests.update(update_dict)

combined_ww2cf = Counter()
client = Client(config.RemoteDirs.root.name, param2default)
for param_path, label in client.gen_param_ps(param2requests, verbose=False):

    print(param_path)

    # get partial co-occurrence counts
    pkl_paths = list(param_path.glob('**/ww2cf.pkl'))
    if len(pkl_paths) == 0:
        raise FileNotFoundError(f'Did not find ww2cf.pkl in {param_path}')
    pkl_path = pkl_paths[0]
    ww2cf = pickle.load(pkl_path.open('rb'))

    # accumulate co-occurrence counts (across multiple jobs)
    partial_ww2cf = Counter(ww2cf)
    combined_ww2cf.update(partial_ww2cf)
    print(combined_ww2cf)