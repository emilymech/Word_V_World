from src.WikiExtractor import main
from src.preprocess1 import remove_tags


class Args:
    json = False
    namespaces = ''  # this is the default


def save_to_text():
    out_titles_p = Path.cwd() / 'titles.txt'
    out_bodies_p = Path.cwd() / 'bodies.txt'

    f1 = out_titles_p.open('w')
    f2 = out_bodies_p.open('w')

    for body, title in zip(bodies, titles):
        flattened = re.sub('\n+', ' ', body)

        f1.write(title + '\n')
        f2.write(flattened + '\n')


def cluster_job(param2val):  # ENTRY POINT
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