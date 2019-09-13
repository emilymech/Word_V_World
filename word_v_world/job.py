from word_v_world.WikiExtractor import main
from word_v_world.preprocess1 import remove_tags


class Args:
    json = False
    toHTML = False
    acceptedNamespaces = ['w', 'wiktionary', 'wikt']
    moduleNamespace = ''
    templateNamespace = ''
    templatePrefix = ''
    knownNamespaces = {'Template': 10}
    namespaces = ''  # this is the default
    keep_tables = True # need to test this out
    keepSections = True # need to test this out
    keepLists = True # need to test this out
    min_text_length = 0
    print_revision = False
    escape_doc = False
    expand_templates = True
    filter_disambig_pages = False
    urlbase = ''
    -b = "50M" #need to double check if these arguments need to be written in the format of the main or the simple namespace



def save_to_text():
    out_titles_p = Path.cwd() / 'titles.txt'
    out_bodies_p = Path.cwd() / 'bodies.txt'

    f1 = out_titles_p.open('w')
    f2 = out_bodies_p.open('w')

    for body, title in zip(bodies, titles):
        flattened = re.sub('\n+', ' ', body)

        f1.write(title + '\n')
        f2.write(flattened + '\n')


def main(param2val):  # ENTRY POINT
    #   use this integer to index into list of wikipedia chunks
    part = param2val['part']

    print('Starting the cluster job')
    args = Args()
    assert not hasattr(args, 'part')  # safety check
    args.part = part

    # step 1
    cleaned = main(args)  # cleaning - this shouldn't output anything - keep result in memory
    # TODO make sure to return the "cleaned" object

    # step 2
    remove_tags(cleaned)

    # step 3
    save_to_text()  # saves to compute node but not server (inaccessible)

    # step 4 - copy text files to server