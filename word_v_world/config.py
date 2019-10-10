from pathlib import Path

from ludwig.config import mnt_point


class RemoteDirs:
    """
    Typically, when using LudwigCluster to execute code, root should always be /media/research_data
     regardless of user's OS.
    However, when user intends to execute code on host only, and intends to retrieve data from shared drive,
     and has MacOS, root must be changed to something like /Volumes/research_data

    """
    research_data = Path(mnt_point) / 'research_data'
    root = research_data / 'Word_V_World'
    runs = root / 'runs'
    wiki = research_data / 'CreateWikiCorpus'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'word_v_world'
    runs = root / '{}_runs'.format(src.name)

    wiki = Path('/home/ph') / 'CreateWikiCorpus'  # TODO user must edit this


class Global:
    debug = False
    min_article_length = 1


class Default:

    # this is the default parameter configuration for filtering paths to bodies.txt files
    param2requests = {'part': [0, 1, 2, 3, 4, 5, 6],
                      'num_machines': [7],
                      'input_file_name': ['dummy_input.xml']}