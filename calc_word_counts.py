import matplotlib.pyplot as plt
import operator
import re


# from word_v_world.articles import get_paths_to_articles, generate_articles
from word_v_world.stats import make_word2frequency
import tokenize_articles

NUM_ARTICLES = 1  # total articles in 1/7 corpus evaluated here: 847,505 (10/11/19), 5934163 in total
NUM_WORDS = 100


# make a list of words in all articles
all_words = tokenize_articles.tokenize(NUM_ARTICLES)

# count word frequencies
w2f = make_word2frequency(all_words)

# count the enters in the corpus

# TODO below is incorrect - the if-statement evaluates to True every time!
# TODO: you need to: if word == \n: count_enters += 1

count_enters = 0
for word in all_words:
    if '\n':
        count_enters += 1
print("Number of enters:", count_enters)


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
plt.show()
