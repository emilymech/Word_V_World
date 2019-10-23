import pickle


from word_v_world import config

NUM_WORDS = 100
NUM_LUDWIG_WORKERS = 6
file_name = 'w2dfs_4800_ALL.pkl'
wiki_param_name = ['param_{}'.format(22 + i) for i in range(NUM_LUDWIG_WORKERS)]


# get the pickle for each param folder individually
def get_pickles(wiki_param_name, w2dfs_file_name):
    wiki_param_path = config.RemoteDirs.wiki / 'runs' / wiki_param_name
    if not wiki_param_path.exists():
        raise FileNotFoundError('{} does not exist'.format(wiki_param_name))
    full_path = wiki_param_path / w2dfs_file_name
    with full_path.open('rb') as file:
        w2dfs = pickle.load(file)
    return w2dfs  # this is a list of dicts by article in params


def make_dict_lowercase(dict):
    dict_lower = {k.lower(): v for k, v in dict.items()}
    return dict_lower


# loop over each individual pickle and add unique keys to dictionaries/update values of non-unique keys
def make_master_dict(wiki_param_name):
    master_dict = {}
    for param in wiki_param_name:
        print("Adding {}".format(param))
        current_w2dfs = get_pickles(param, file_name)
        for current_dict in current_w2dfs:
            lower_dict = make_dict_lowercase(current_dict)
            for key in lower_dict:
                if lower_dict[key] in master_dict:
                    master_dict[key] += lower_dict[key]
                else:
                    master_dict[key] = lower_dict[key]
                # print("New size is {}".format(len(master_dict)))
    return master_dict


# sort the freq dicts
def sorted_freq_dict(dict):
    freq_list = [(dict[key], key) for key in dict]
    freq_list.sort()
    freq_list.reverse()
    for n, pair in enumerate(freq_list):
        if n == NUM_WORDS:
            break
        print(str(pair))
    return freq_list


def main():
    sorted_freq_dict(make_master_dict(wiki_param_name))
    return


main()
