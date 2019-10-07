

from word_v_world.articles import get_paths_to_articles, generate_articles
from word_v_world.stats import make_word2frequency

NUM_ARTICLES = 3
NUM_WORDS = 10
PARAM2REQUESTS = None


paths_to_articles = []
for p in get_paths_to_articles(param2requests=PARAM2REQUESTS):
    print(p)
    paths_to_articles.append(p)

# make a list of words in all articles
all_words = []
for article in generate_articles(paths_to_articles, num_articles=NUM_ARTICLES):
    words = article.split(' ')
    all_words += words

# count word frequencies
w2f = make_word2frequency(all_words)

# print ten most frequent words
for n, (w, f) in enumerate(w2f.items()):  # dictionary is ordered by freq
    if n == NUM_WORDS:
        break

    print('{:<20} {}'.format(w, f))
