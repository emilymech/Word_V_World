
from word_v_world import config


def generate_articles(path=None):
    """
    a generator that yields wiki articles.
    :return: a generator of articles, (str, str, ...)
    """
    if path is None:
        path = config.RemoteDirs.wiki

    print('Looking for text files in {}'.format(path))

    for titles_path in path.rglob('bodies.txt'):
        print('Adding words from {}'.format(titles_path))
        articles = titles_path.read_text()
        for article in articles.split('\n'):
            yield article
