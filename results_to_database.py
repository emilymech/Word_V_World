import pickle
import sqlite3
from pathlib import Path

from ludwig.results import gen_param_paths

from word_v_world import config
from word_v_world.params import param2requests, param2default, param2debug

MINIMAL = False
VERBOSE = True

''' To Update:
    1. Update params in the update_dict dictionary
    2. Update database name'''

#  TODO - run ws 7, sum (all ws 4 are done), run ws 1, summed
# Done: All ws 4
#       backward 1

# specify which parameter configuration for which to retrieve results
update_dict = {
    'cwc_param_name': ['param_22', 'param_23', 'param_24', 'param_25', 'param_26', 'param_27'],
    'num_machines': [6],
    'article_coverage': [1.0],
}
param2requests.update(update_dict)

if MINIMAL:
    param2requests.update({k: [v] for k, v in param2debug.items()})

# get paths from which to load co-occurrence data
project_name = Path.cwd().name
paths_to_n2c2f = []
for param_path, label in gen_param_paths(project_name,
                                         param2requests,
                                         param2default,
                                         research_data_path=config.Dirs.research_data,
                                         verbose=False):
    pkl_paths = list(param_path.glob('**/saves/n2c2f.pkl'))
    if len(pkl_paths) == 0:
        raise FileNotFoundError(f'Did not find n2c2f.pkl in {param_path}')
    else:
        print(f'Found {pkl_paths[0]}')
    paths_to_n2c2f.append(pkl_paths[0])

# create database
db_name = 'noun_child_cooc.sqlite'
conn = sqlite3.connect(db_name)
c = conn.cursor()
try:
    c.execute('CREATE TABLE cfs (w1 text, w2 text, cf integer)')
except sqlite3.OperationalError:   # table already exists
    pass

# populate database
for path_to_n2c2f in paths_to_n2c2f:
    print(f'Adding co-occurrence data from {path_to_n2c2f} to {db_name}')

    f = path_to_n2c2f.open('rb')
    try:
        partial_n2c2f = pickle.load(f)
    except MemoryError as e:
        raise MemoryError('Reached memory limit')
    except KeyboardInterrupt:
        f.close()
        conn.close()
        raise KeyboardInterrupt

    # add to database
    for n, c2f in partial_n2c2f.items():
        for child in c2f:
            values = (n, child, c2f[child])
            command = "INSERT INTO cfs VALUES (?, ?, ?)"
            if VERBOSE:
                print(values)
            c.execute(command, values)

    # remove no longer needed object
    del partial_n2c2f

conn.commit()  # save changes
conn.close()
print('Saved changes and closed database.')
