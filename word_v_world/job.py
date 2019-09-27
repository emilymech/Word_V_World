import re
from multiprocessing import cpu_count

from wikiExtractor.WikiExtractor import extract_from_wiki
from word_v_world.remove_tags import remove_tags
from word_v_world.params import param2default
from word_v_world import config


class Args:
    bytes = "50M"
    compress = False
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
    keep_tables = False
    processes = max(1, cpu_count() - 1)
    quiet = False
    debug = False
    article = False
    log_file = False
    version = False
    filter_category = None


def save_text_to_shared_drive(titles, bodies, param2val):
    job_name = config.RemoteDirs.runs / param2val['param_name'] / param2val['job_name']
    if not job_name.is_dir():
        job_name.mkdir(parents=True)  # this is not ideal, because folders are created before job has completed
    out_titles_p = job_name / 'titles.txt'
    out_bodies_p = job_name / 'bodies.txt'

    f1 = out_titles_p.open('w')
    f2 = out_bodies_p.open('w')

    for body, title in zip(bodies, titles):
        flattened = re.sub('\n+', ' ', body)

        f1.write(title + '\n')
        f2.write(flattened + '\n')


def main(param2val):  # param2val will be different on each machine

    part = param2val['part']
    num_machines = param2val['num_machines']
    input_file_name = param2val['input_file_name']

    # step 1
    print('Word_V_World: Starting extraction with part={} and num_machines={}'.format(part, num_machines))
    Args.input = str(config.RemoteDirs.data / input_file_name)  # always put xml file on shared drive
    Args.output = str(config.LocalDirs.wiki_output)  # folder on ludwig worker (not on shared drive)
    extract_from_wiki(Args, part, num_machines)  # this saves extracted pages to worker

    # step 2
    print('Word_V_World: Starting removal of html tags...')
    titles, bodies = remove_tags(Args.output)

    # step 3
    print('Word_V_World: Saving to text...')
    save_text_to_shared_drive(titles, bodies, param2val)

    return []  # ludwigcluster requires a list (empty, or containing pandas dataframes)
