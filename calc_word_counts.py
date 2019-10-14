import matplotlib.pyplot as plt
import operator


from word_v_world.articles import get_paths_to_articles, generate_articles
from word_v_world.stats import make_word2frequency
from tokenize_articles import tokens

NUM_ARTICLES = 50  # total articles in 1/7 corpus evaluated here: 847,505 (10/11/19), 5934163 in total
NUM_WORDS = 200
PARAM2REQUESTS = {'part': [0, 1, 2, 3, 4, 5, 6],
                  'num_machines': [7],
                  'input_file_name': ['enwiki-20190920-pages-articles-multistream.xml.bz2']}
# user can overwrite default by overwriting None
# TODO need to ask Phil about how to change this from "None" the right way ^

paths_to_articles = []
for p in get_paths_to_articles(param2requests=PARAM2REQUESTS):
    paths_to_articles.append(p)


# make a list of words in all articles
all_words = []
for article in generate_articles(paths_to_articles, num_articles=NUM_ARTICLES):
    words = tokens
    all_words += words

# count word frequencies
w2f = make_word2frequency(all_words)

# print most frequent words and plot them (at cut-offs of: 4096, 8192, 16384, 32768)
for n, (w, f) in enumerate(w2f.items()):  # dictionary is ordered by freq
    if n == NUM_WORDS:
        break

    print('{:<20} {}'.format(w, f))


def word_freq():
    freq_list = make_word2frequency(all_words)
    freq = enumerate(freq_list.items())
    sorted_wiki_freqs = (sorted(freq.items(), key=operator.itemgetter(1)))[::-1]
    word = "the"
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

    plt.title("Word Frequencies in " + sorted_wiki_freqs)
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
    plt.show()



