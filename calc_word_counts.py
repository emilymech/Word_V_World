import spacy
from collections import Counter, OrderedDict

from word_v_world import config


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


all_words = []

print('Looking for text files in {}'.format(config.RemoteDirs.wiki))
for titles_path in config.RemoteDirs.wiki.rglob('bodies.txt'):
    print('Adding words from {}'.format(titles_path))
    text = titles_path.read_text().replace('\n', ' ')
    words = text.split(' ')
    all_words += words

# count word frequencies
w2f = make_word2frequency(all_words)

# print ten most frequent words
for n, (w, f) in enumerate(w2f.items()):  # dictionary is ordered by freq
    if n == 10:
        break

    print('{:<20} {}'.format(w, f))
