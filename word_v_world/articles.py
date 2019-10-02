
from word_v_world import config


def generate_articles(path=None, num_articles=None):
    """
    a generator that yields wiki articles.
    :return: a generator of articles, (str, str, ...)
    """
    if path is None:
        path = config.RemoteDirs.wiki

    print('Looking for text files in {}'.format(path))

    counter = 0

    for bodies_path in path.rglob('bodies.txt'):
        print('Adding words from {}'.format(bodies_path))
        f = bodies_path.open('r')
        for article in f:
            yield article

            counter += 1
            if num_articles is not None:
                if counter == num_articles:
                    return
