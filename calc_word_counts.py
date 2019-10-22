import matplotlib.pyplot as plt
import operator
import pickle

from word_v_world import config


NUM_WORDS = 100
NUM_LUDWIG_WORKERS = 6
file_name = 'w2dfs_4800_ALL.pkl'
wiki_param_name = ['param_{}'.format(22 + i) for i in range(NUM_LUDWIG_WORKERS)]


def get_pickles(wiki_param_name, w2dfs_file_name):
    wiki_param_path = config.RemoteDirs.wiki / 'runs' / wiki_param_name
    if not wiki_param_path.exists():
        raise FileNotFoundError('{} does not exist'.format(wiki_param_name))
    full_path = wiki_param_path / w2dfs_file_name
    with full_path.open('rb') as file:
        w2dfs = pickle.load(file)
    return w2dfs  # works for params/files specified 1 at a time


# can we concatenate all of the pickle objects? (redundant with above/debugging this function)
# TODO - figure out how to loop through all of the param folders and concatenate/merge pickles
def get_pickle_paths(wiki_param_name, w2dfs_file_name):
    pickle_paths = []
    for param in wiki_param_name:
        path_to_pickle = list(param.glob('**/w2dfs_4800_ALL.pkl'))[0]
        pickle_paths.append(path_to_pickle)

    wiki_param_path = [config.RemoteDirs.wiki / 'runs' / wiki_param_name]
    for path in wiki_param_path:
        if not wiki_param_path.exists():
            raise FileNotFoundError('{} does not exist'.format(wiki_param_name))
        full_path = wiki_param_path / w2dfs_file_name
        with full_path.open('rb') as file:
            w2dfs = pickle.load(file)
    return w2dfs


# sort the freq dicts
# TODO - fix this function once the dicts are figured out
def sort_freq_dict(NUM_WORDS):
    sorted_wiki_freqs = (sorted(w2dfs.items(), key=operator.itemgetter(1)))[::-1]
    for n, (w, f) in sorted_wiki_freqs:
        if n == NUM_WORDS:
            break
        print('{:<20} {}'.format(w, f))


# make a frequency plot
def plot(file_name):
    freq_list = file_name
    sorted_wiki_freqs = (sorted(freq_list.items(), key=operator.itemgetter(1)))[::-1]
    word = "at"
    just_the_occur = []
    just_the_rank = []
    word_rank = 0
    word_frequency = 0

    entry_num = 1
    for entry in sorted_wiki_freqs:

        if entry[0] == word:
            word_rank = entry_num
            word_frequency = entry[1]

        just_the_rank.append(entry_num)
        entry_num += 1
        just_the_occur.append(entry[1])

    plt.title("Word Frequencies in Wiki Corpus")
    plt.ylabel("Total Number of Occurrences")
    plt.xlabel("Rank of word(\"" + word + "\" is rank " + str(word_rank) + ")")
    plt.loglog(
        just_the_rank,
        just_the_occur,
        basex=10
    )
    plt.scatter(
        [word_rank],
        [word_frequency],
        color="orange",
        marker="*",
        s=100,
        label=word
    )
    return plt.show()
