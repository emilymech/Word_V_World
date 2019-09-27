import spacy
from collections import Counter, OrderedDict

from word_v_world import config


def word2frequency(words):
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


all_bodies = []

print('Looking for text files in {}'.format(config.RemoteDirs.wiki))
for bodies_path in config.RemoteDirs.wiki.rglob('bodies.txt'):

    with bodies_path.open('r') as f:
        bodies = f.readlines()
        print(bodies[0])

    all_bodies += bodies