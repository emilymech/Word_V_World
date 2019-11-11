import pickle
import sqlite3
from pathlib import Path

from ludwig.results import gen_param_paths

from word_v_world import config
from word_v_world.memory import set_memory_limit
from word_v_world.params import param2requests, param2default, param2debug

MINIMAL = False

# specify which parameter configuration for which to retrieve results
update_dict = {
    'cwc_param_name': ['param_22', 'param_23', 'param_24', 'param_25', 'param_26', 'param_27'],
    'num_machines': [6],
    'vocab_name': ['100000_vocab_20191108_15-17-19'],
    'article_coverage': [0.25]
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

set_memory_limit(prop=0.9)

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
        c.execute("INSERT INTO cfs VALUES (?, ?, ?)", values)
    # remove no longer needed object
    del partial_ww2cf

    break  # TODO test

conn.commit()  # save changes
conn.close()


# TODO each duplicate key is given a separate entry - but cfs must be added

# TODO ideally, this script should be run directly on server to prevent loading data over network