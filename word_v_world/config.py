from pathlib import Path
import sys

if sys.platform == 'darwin':
    mnt_point = '/Volumes'
elif 'win' in sys.platform:
    raise SystemExit('LudwigCluster does not support Windows')
elif 'linux' == sys.platform:
    mnt_point = '/media'


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


class Global:
    debug = False
    min_article_length = 1