

def get_text_file_path(param_path, pattern):
    """
    return path to bodies.txt or titles.txt depending on "pattern"
    """
    bodies_paths = list(param_path.glob(f'**/{pattern}.txt'))
    if len(bodies_paths) == 0:
        raise SystemExit('Did not find bodies.txt in {}'.format(param_path))
    elif len(bodies_paths) > 1:
        raise SystemExit('Found more than one path to articles')
    else:
        return bodies_paths[0]


def generate_articles(bodies_path):
    """
    a generator that yields wiki articles from a single file
    """
    print('Reading articles from {}'.format(bodies_path))

    with bodies_path.open('r') as f:
        for article in f:
            yield article