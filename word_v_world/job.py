from pathlib import Path
import re
from multiprocessing import cpu_count

from word_v_world.WikiExtractor import extract_from_wiki
from word_v_world.remove_tags import remove_tags
from word_v_world import config


class Args:
    input = 'enwiki-20190801-pages-articles-multistream24.xml-p33503454p33952815'
    output = config.Global.output
    bytes = "50M"
    compress = False
    json = False
    html = False
    links = False
    sections = False
    lists = False
    namespaces = ""
    templates = {}
    no_templates = True
    revision = False
    min_text_length = 0
    filter_disambig_pages = False
    ignored_tags = ""
    discard_elements = ""
    keep_tables = True
    processes = max(1, cpu_count() - 1)
    quiet = False
    debug = False
    article = False
    log_file = False
    version = False
    filter_category = None


def save_to_text(bodies, titles):
    out_titles_p = Path.cwd() / 'titles.txt'
    out_bodies_p = Path.cwd() / 'bodies.txt'

    f1 = out_titles_p.open('w')
    f2 = out_bodies_p.open('w')

    for body, title in zip(bodies, titles):
        flattened = re.sub('\n+', ' ', body)

        f1.write(title + '\n')
        f2.write(flattened + '\n')


def main(param2val):  # param2val will be different on each machine

    part = param2val['part']
    num_machines = param2val['num_machines']
    print('Word_V-World: Starting extraction with part={} and num_machines={}'.format(part, num_machines))

    # step 1
    extract_from_wiki(Args, part, num_machines)  # this saves extracted pages to disk

    # step 2
    print('Word_V-World: Starting removal of html tags...')
    titles, bodies = remove_tags(Args.output)

    print(titles[0])
    print(bodies[0])
    raise SystemExit

    # step 3
    save_to_text()  # saves to compute node but not server (inaccessible)

    # step 4 - copy text files to server