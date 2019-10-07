from itertools import islice
import sys
import importlib

from word_v_world import config

from ludwig.client import Client


def get_paths_to_articles(param2requests=None, print_size=True):
    """
    generate path objects pointing to only those bodies.txt files which are associated with param2val.yaml
    that contains the run configuration we are interested in (as specified in param2requests)
    """

    if param2requests is None:
        param2requests = config.Default.param2requests

    # TODO check that PARAM2REQUESTS only allows 1 corpus to be made
    #  which means that at the most 7 param2vals are allowed to be created from PARAM2REQUESTS

    # load params module from CreateWikiCorpus (CreateWikiCorpus/createwikicorpus/params.py)
    if not config.LocalDirs.wiki.exists():
        raise FileNotFoundError('{} does not exist.'.format(config.LocalDirs.wiki))
    else:
        print('Appending {} to sys.path'.format(config.LocalDirs.wiki))
    sys.path.append(str(config.LocalDirs.wiki))
    wiki_params = importlib.import_module('createwikicorpus.params')

    # loop over only those bodies.txt files which are associated with param2val.yaml that contains
    # the configuration we are interested in (as specified in param2requests)
    client = Client('CreateWikiCorpus', wiki_params.param2default)
    allowed_paths = []
    for param_p, label in client.gen_param_ps(param2requests, verbose=False):
        path_to_article = list(param_p.glob('**/bodies.txt'))[0]
        allowed_paths.append(path_to_article)
        print('Request matches {}'.format(path_to_article))

        # optional: measure size of bodies.txt file in MBs
        if print_size:
            num_bytes = path_to_article.stat().st_size
            num_megabytes = num_bytes >> 20
            print('{} contains {} MBs'.format(path_to_article.relative_to(config.RemoteDirs.research_data),
                                              num_megabytes))
            print()

        yield path_to_article


def generate_articles(paths_to_articles, num_articles=None):
    """
    a generator that yields wiki articles.
    :return: a generator of articles, (str, str, ...)
    """
    print('Looking for text files in {}'.format(config.RemoteDirs.wiki))

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


def generate_articles_from_slice(start, stop, **kwargs):
    for article in islice(generate_articles(**kwargs), start, stop):
        yield article