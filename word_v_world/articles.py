
def get_text_file_path(param_path, pattern):
    """
    return path to bodies.txt or titles.txt depending on "pattern"
    """
    glob_pattern = f'**/{pattern}.txt'
    bodies_paths = list(param_path.glob(glob_pattern))
    if len(bodies_paths) == 0:
        raise SystemExit(f'Did not find {pattern}.txt in {param_path}')
    elif len(bodies_paths) > 1:
        raise SystemExit('Found more than one path to articles')
    else:
        return bodies_paths[0]


def generate_articles(bodies_path, max_num_characters):
    """
    a generator that yields wiki articles from a single file
    """
    print('Reading articles from {}'.format(bodies_path))

    num_skipped = 0
    with bodies_path.open('r') as f:
        for article in f:

            if len(article) > max_num_characters:
                num_skipped += 1
                continue

            yield article.strip('\n')

    print(f'Skipped {num_skipped} articles')
