import pickle
import shelve
from pathlib import Path

from ludwig.results import gen_param_paths

from word_v_world import config
from word_v_world.memory import set_memory_limit
from word_v_world.params import param2requests, param2default

# specify which parameter configuration for which to retrieve results
update_dict = {
    'cwc_param_name': ['param_22', 'param_23', 'param_24', 'param_25', 'param_26', 'param_27'],
    'num_machines': [6],
    'vocab_name': ['100000_vocab_20191108_15-17-19'],
    'article_coverage': [0.25]
}
param2requests.update(update_dict)

# get paths from which to load co-occurrence data
project_name = Path.cwd().name
paths_to_ww2cf = []
for param_path, label in gen_param_paths(project_name,
                                         param2requests,
                                         param2default,
                                         research_data_path=config.LocalDirs.research_data,
                                         verbose=False):
    pkl_paths = list(param_path.glob('**/saves/ww2cf.pkl'))
    if len(pkl_paths) == 0:
        raise FileNotFoundError(f'Did not find ww2cf.pkl in {param_path}')
    else:
        print(f'Found {pkl_paths[0]}')
    paths_to_ww2cf.append(pkl_paths[0])

set_memory_limit(prop=0.9)

# accumulate co-occurrence counts (across multiple jobs) in database
s = shelve.open('test_shelf.db')
for path_to_ww2cf in paths_to_ww2cf:
    print(f'Accumulating co-occurrence data from {path_to_ww2cf}')

    f = path_to_ww2cf.open('rb')
    try:
        partial_ww2cf = pickle.load(f)
    except MemoryError as e:
        raise MemoryError('Reached memory limit')
    except KeyboardInterrupt:
        f.close()
    else:
        del partial_ww2cf

        # TODO add to database
        for ww, cf in partial_ww2cf.items():
            s[ww] = cf



    break  # TODO test

print(s[('the', 'on')])


