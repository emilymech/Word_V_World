from pathlib import Path
import socket

# from ludwig.config import mnt_point


class RemoteDirs:
    """
    Typically, when using LudwigCluster to execute code, research_data should always be /media/research_data
     regardless of user's OS.
    However, when user intends to execute code on host only, and intends to retrieve data from shared drive,
     and has MacOS, root must be changed to something like /Volumes/research_data

    """
    research_data = Path('/media') / 'research_data'
    root = research_data / 'Word_V_World'
    runs = root / 'runs'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'word_v_world'
    runs = root / '{}_runs'.format(src.name)

    # TODO this is a hack - use .env file and dot_env package to remedy

    if socket.gethostname() == 'wirelessprv-10-195-203-206.near.illinois.edu':
        wiki = Path('/Volumes/GoogleDrive/My Drive/UIUC/PyCharm') / 'CreateWikiCorpus'
    elif socket.gethostname() == 'Emilys-MacBook-Pro.local':
        wiki = Path('/Volumes/GoogleDrive/My Drive/UIUC/PyCharm') / 'CreateWikiCorpus'
    else:
        wiki = Path('/home/ph/CreateWikiCorpus')


class Global:
    debug = False
