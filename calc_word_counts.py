from collections import Counter, OrderedDict

from word_v_world.articles import generate_articles


def make_word2frequency(words):
    """
    input is a list of words
    returns a dictonary mapping a word to its frequency

    words: List[str]
    return: Dict[str, frequency]
    """
    c = Counter(words)
    result = OrderedDict(
        sorted(c.items(), key=lambda item: (item[1], item[0]), reverse=True))  # order matters
    return result


# make a list of words in all articles
all_words = []
for article in generate_articles():
    words = article.split(' ')
    all_words += words

# count word frequencies
w2f = make_word2frequency(all_words)

# print ten most frequent words
for n, (w, f) in enumerate(w2f.items()):  # dictionary is ordered by freq
    if n == 10:
        break

    print('{:<20} {}'.format(w, f))
