from itertools import islice


def generate_articles(paths_to_articles, num_articles = None):
    """
    a generator that yields wiki articles.
    :return: a generator of articles, (str, str, ...)
    """
    print('Looking for text files...')

    if not paths_to_articles:
        raise ValueError('"paths_to_articles" is empty.')

    counter = 0
    for article_path in paths_to_articles:
        print('Reading articles from {}'.format(article_path))

        f = article_path.open('r')
        for article in f:
            yield article

            counter += 1
            if num_articles is not None:
                if counter == num_articles:
                    return


def generate_articles_from_slice(paths_to_articles, start, stop, **kwargs):
    for article in islice(generate_articles(paths_to_articles, **kwargs), start, stop):
        yield article
