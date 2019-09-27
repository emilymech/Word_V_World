import re

from word_v_world import config


def remove_tags(output_folder_name):
    files_path = config.LocalDirs.root / output_folder_name
    print('Removing tags from articles in {}'.format(files_path))

    num_articles = 0
    titles = []
    bodies = []

    for file in files_path.rglob('wiki_*'):
        print('-Removing tags from articles in {}'.format(file.name))
        text = file.read_text()

        compiled = re.compile('\n*.*<doc id=".*" url=".*" title=".*">\n([^\n]*)(.*\n*$)',
                              flags=re.S)  # make dot match newline
        articles = re.split('</doc>', text)
        num_articles += len(articles)

        for article in articles:

            if len(article) > config.Global.min_article_length:
                res = compiled.match(article)
                title = res.groups()[0]
                body = res.groups()[1]

                titles.append(title)
                bodies.append(body)

    assert len(bodies) == len(titles)
    print('Removed tags from {} articles'.format(num_articles))

    return titles, bodies