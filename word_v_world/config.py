from pathlib import Path
import sys

is_linux = sys.platform == 'linux'


class RemoteDirs:
    root = Path('/{}/research_data'.format('media' if is_linux else 'Volumes')) / 'Word_V_World'
    runs = root / 'runs'
    data = root / 'data'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'word_v_world'
    runs = root / '{}_runs'.format(src.name)
    wiki_output = root / 'output'


class Global:
    debug = False
    min_article_length = 1