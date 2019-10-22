import matplotlib.pyplot as plt
import operator
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


# loop over each individual pickle and add unique keys to dictionaries/update values of non-unique keys
def make_master_dict(wiki_param_name):
    master_dict = {}
    for param in wiki_param_name:
        print("Adding {}".format(param))
        current_w2dfs = get_pickles(param, file_name)
        # print(current_w2dfs)
        for current_dict in current_w2dfs:
            for key in current_dict:
                if current_dict[key] in master_dict:
                    master_dict[key] += current_dict[key]
                else:
                    master_dict[key] = current_dict[key]
                # print("New size is {}".format(len(master_dict)))
                return master_dict


print("This is master_dict", make_master_dict(wiki_param_name))  # TODO - fix make_master_dict

# sort the freq dicts
# TODO - fix this function once the dicts are figured out
def sorted_freq_dict(master_dict):
    sorted_wiki_freqs = (sorted(master_dict.items(), key=operator.itemgetter(1)))[::-1]
    for n, (w, f) in sorted_wiki_freqs:
        if n == NUM_WORDS:
            break
        print('{:<20} {}'.format(w, f))
        return sorted_wiki_freqs


# make a frequency plot
def plot(master_freq_dict):
    word = "at"
    just_the_occur = []
    just_the_rank = []
    word_rank = 0
    word_frequency = 0

    entry_num = 1
    for entry in master_freq_dict:

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


def main():
    sorted_master_dict = sorted_freq_dict(make_master_dict(wiki_param_name))
    freq_plot = plot(sorted_freq_dict(make_master_dict(wiki_param_name)))
    print(sorted_master_dict)
    print(freq_plot)
    return


main()
