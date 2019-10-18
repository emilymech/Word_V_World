import matplotlib.pyplot as plt
import operator

# TODO - once the all words count is done, need to strip punctuation
# TODO - get rid of any counting in this and import the pickle object for the already counted items

# from word_v_world.articles import get_paths_to_articles, generate_articles
from word_v_world.stats import make_word2frequency
from word_v_world import tokenization

NUM_ARTICLES = 1  # total articles in 1/7 corpus evaluated here: 847,505 (10/11/19), 5934163 in total
NUM_WORDS = 100

# tokenization
paths_to_articles = tokenization.get_path()

# make a list of words in all articles
all_words = tokenization.tokenize(NUM_ARTICLES, paths_to_articles)

# count word frequencies
w2f = make_word2frequency(all_words)


# print most frequent words and plot them (at cut-offs of: 4096, 8192, 16384, 32768)
for n, (w, f) in enumerate(w2f.items()):  # dictionary is ordered by freq
    if n == NUM_WORDS:
        break

    print('{:<20} {}'.format(w, f))


# make a frequency plot
freq_list = make_word2frequency(all_words)
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
# plt.show()
