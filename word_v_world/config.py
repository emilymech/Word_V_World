from pathlib import Path
import sys

is_linux = sys.platform == 'linux'


class RemoteDirs:
    """
    Typically, when using LudwigCluster to execute code, root should always be /media/research_data
     regardless of user's OS.
    However, when user intends to execute code on host only, and intends to retrieve data from shared drive,
     and has MacOS, root must be changed to something like /Volumes/research_data

    """
    root = Path('/{}/research_data'.format('media' if is_linux else 'Volumes')) / 'Word_V_World'
    runs = root / 'runs'
    wiki = Path('/{}/research_data'.format('media' if is_linux else 'Volumes')) / 'CreateWikiCorpus'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'word_v_world'
    runs = root / '{}_runs'.format(src.name)


class Global:
    debug = False
    min_article_length = 1