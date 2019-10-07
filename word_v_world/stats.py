from collections import Counter, OrderedDict


def make_word2frequency(words):
    """
    input is a list of words
    returns a dictionary mapping a word to its frequency

    words: List[str]
    return: Dict[str, frequency]
    """
    c = Counter(words)
    result = OrderedDict(
        sorted(c.items(), key=lambda item: (item[1], item[0]), reverse=True))  # order matters
    return result