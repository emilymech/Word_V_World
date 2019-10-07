from itertools import islice

from word_v_world import config
from word_v_world.filter import allowed_paths


def generate_articles(path_to_wiki_root=None, num_articles=None):
    """
    a generator that yields wiki articles.
    :return: a generator of articles, (str, str, ...)
    """
    if path_to_wiki_root is None:
        path_to_wiki_root = config.RemoteDirs.wiki

    print('Looking for text files in {}'.format(path_to_wiki_root))

    counter = 0

    for bodies_path in path_to_wiki_root.rglob('bodies.txt'):
        print('Reading articles from {}'.format(bodies_path))

        # TODO filter by _param_name

        if bodies_path not in allowed_paths:
            continue

        f = bodies_path.open('r')
        for article in f:
            yield article

            counter += 1
            if num_articles is not None:
                if counter == num_articles:
                    return


def generate_articles_from_slice(start, stop, **kwargs):
    for article in islice(generate_articles(**kwargs), start, stop):
        yield article