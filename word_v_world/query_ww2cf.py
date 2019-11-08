import numpy as np

from word_v_world import config
from data.pairs import act_pairs, adj_pairs, ass_pairs, curious_pairs, part_pairs

# TODO - generate yaml for each pair run and add unique date/time id
# TODO - visualize co-oc matrix


# get co-occurrence counts for these word pairs
def query_by_key(wiki_dictionary):
    with (config.LocalDirs.root / 'output' / 'adj_co_query-UNIQUEID.txt').open('w') as f:
        for pair in adj_pairs.adj_co_query:
            print(pair, wiki_dictionary.get(pair, None))
        f.write(str((pair, wiki_dictionary.get(pair, None))) + '\n')
    return


# search for all keys that have a given value
def query_by_value(wiki_dictionary):
    for pair, cf in wiki_dictionary.items():
        if cf < 100:
            print(pair, cf)
    return


# get dictionary descriptives
def get_descriptives(wiki_dictionary):
    mean_value = np.array(list(wiki_dictionary.values())).mean()
    print("This is the mean of the values:", mean_value)

    max_value = max(wiki_dictionary.keys(), key=(lambda k: wiki_dictionary[k]))
    print("This is the maximum value:", wiki_dictionary[max_value])

    min_value = min(wiki_dictionary.keys(), key=(lambda k: wiki_dictionary[k]))
    print("This is the minimum value:", wiki_dictionary[min_value])

    return
