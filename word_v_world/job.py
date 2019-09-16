from pathlib import Path
import re

from word_v_world.WikiExtractor import extract_from_wiki, pages_from
from word_v_world.preprocess1 import remove_tags


class Args:

    # doesn't need 'input' because we are explicitly passing the input (a part of the input)
    input = '../Wiki_data/enwiki-20190801-pages-articles-multistream24.xml-p33503454p33952815'
    output = 'text'
    bytes = "50M"
    compress = True
    json = False
    html = False
    links = False
    sections = True
    lists = True
    namespaces = ""
    templates = {}
    no_templates = True
    revision = False
    min_text_length = 0
    filter_disambig_pages = False
    ignored_tags = ""
    discard_elements = ""
    keep_tables = True
    processes = "default_process_count"
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


def get_part(all_pages, param2val):
    num_pages_in_part = len(all_pages) // param2val['num_machines']  # the same for each machine

    start_id = param2val['part'] * num_pages_in_part  # different for each machine because 'part' is different
    stop_id = start_id + num_pages_in_part
    return all_pages[start_id:stop_id]


def main(param2val):  # param2val will be different on each machine
    print('Starting the Wiki extracting + cleaning job')
    assert not hasattr(Args, 'part')  # safety check

    # step 1
    print('Word_V-World: Starting extraction...')
    part = param2val['part']
    extract_from_wiki(Args, part)  # this saves extracted pages to disk

    # step 2
    print('Word_V-World: Starting removal of html tags...')
    titles, bodies = remove_tags(Args.output)

    print(titles)
    print(bodies)
    raise SystemExit

    # step 3
    save_to_text()  # saves to compute node but not server (inaccessible)

    # step 4 - copy text files to server