import re
from pathlib import Path


def remove_tags(results_folder):
    files_path = Path.cwd().parent / results_folder

    total_articles = 0
    titles = []
    bodies = []

    for file in files_path.rglob('wiki_*'):
        print(file.name)
        text = file.read_text()

        compiled = re.compile('\n*.*<doc id=".*" url=".*" title=".*">\n(.*)\n*(.*)\n*')
        articles = re.split('</doc>', text)
        print(len(articles))
        total_articles += len(articles)
        for article in articles:


            if len(article) > 10:
                res = compiled.match(article)
                title = res.groups()[0]
                body = res.groups()[1]

                titles.append(title)
                bodies.append(body)

    assert len(bodies) == len(titles)
    print('num articles', total_articles)
    return titles, bodies