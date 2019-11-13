import pickle
import sqlite3
from pathlib import Path

from ludwig.results import gen_param_paths

from word_v_world import config
from word_v_world.params import param2requests, param2default, param2debug

MINIMAL = False
VERBOSE = True

# specify which parameter configuration for which to retrieve results
update_dict = {
    'cwc_param_name': ['param_22', 'param_23', 'param_24', 'param_25', 'param_26', 'param_27'],
    'num_machines': [6],
    'vocab_name': ['mcrae_concepts_features_20191112_16-46'],
    'article_coverage': [1.0],
    'window_type': ['backward'],
    'window_size': [4]
}
param2requests.update(update_dict)

if MINIMAL:
    param2requests.update({k: [v] for k, v in param2debug.items()})

# get paths from which to load co-occurrence data
project_name = Path.cwd().name
paths_to_ww2cf = []
for param_path, label in gen_param_paths(project_name,
                                         param2requests,
                                         param2default,
                                         research_data_path=config.Dirs.research_data,
                                         verbose=False):
    pkl_paths = list(param_path.glob('**/saves/ww2cf.pkl'))
    if len(pkl_paths) == 0:
        raise FileNotFoundError(f'Did not find ww2cf.pkl in {param_path}')
    else:
        print(f'Found {pkl_paths[0]}')
    paths_to_ww2cf.append(pkl_paths[0])

# create database
db_name = 'test.sqlite'  # TODO use multiple databases?
conn = sqlite3.connect(db_name)
c = conn.cursor()
try:
    c.execute('CREATE TABLE cfs (w1 text, w2 text, cf integer)')
except sqlite3.OperationalError:   # table already exists
    pass

# populate database
for path_to_ww2cf in paths_to_ww2cf:
    print(f'Adding co-occurrence data from {path_to_ww2cf} to {db_name}')

    f = path_to_ww2cf.open('rb')
    try:
        partial_ww2cf = pickle.load(f)
    except MemoryError as e:
        raise MemoryError('Reached memory limit')
    except KeyboardInterrupt:
        f.close()
        conn.close()
        raise KeyboardInterrupt

    # add to database
    for ww, cf in partial_ww2cf.items():
        values = (ww[0], ww[1], cf.item())  # cf is numpy int32
        command = "INSERT INTO cfs VALUES (?, ?, ?)"
        if VERBOSE:
            print(values)
        c.execute(command, values)

    # remove no longer needed object
    del partial_ww2cf

conn.commit()  # save changes
conn.close()
print('Saved changes and closed database.')
