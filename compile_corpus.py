import importlib
import sys

from word_v_world import config

from ludwig.client import Client

PATH_TO_CREATE_WIKI_CORPUS_ROOT = '/home/ph/CreateWikiCorpus'

# specify parameters to use for retrieving corpus files
PARAM2REQUESTS = {'part': [0, 1, 2, 3, 4, 5, 6],
                  'num_machines': [7],
                  'input_file_name': ['enwiki-20190920-pages-articles-multistream.xml.bz2']}

# TODO check that PARAM2REQUESTS only allows 1 corpus to be made
#  which means that at the most 7 param2vals are allowed to be created from PARAM2REQUESTS

# load params module from CreateWikiCorpus (CreateWikiCorpus/createwikicorpus/params.py)
sys.path.append(PATH_TO_CREATE_WIKI_CORPUS_ROOT)
create_wiki_params = importlib.import_module('createwikicorpus.params')

# loop over only those bodies.txt files which are associated with param2val.yaml that contains
# the configuration we are interested in (as specified in PARAM2REQUESTS)
client = Client('CreateWikiCorpus', create_wiki_params.param2default)
for param_p, label in client.gen_param_ps(PARAM2REQUESTS):
    bodies_path = list(param_p.glob('**/bodies.txt'))[0]

    # measure size of bodies.txt file in MBs
    num_bytes = bodies_path.stat().st_size
    num_megabytes = num_bytes >> 20
    print('{} contains {} MBs'.format(bodies_path.relative_to(config.RemoteDirs.research_data), num_megabytes))
    print()


